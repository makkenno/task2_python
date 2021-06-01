import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime
from webdriver_manager.chrome import ChromeDriverManager

now = datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')
log_file_path = f"./log/log_{now}.log"
# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(ChromeDriverManager().install(), options=options)

def log(text):
    now = datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')
    log_content = f"log: {text} {now}"
    with open(log_file_path, 'a', encoding='utf-8-sig') as f:
      f.write(log_content + '\n')
    print(log_content)

# main処理


def main():
    log("処理開始")
    search_keyword = input("検索ワードを入力してください >>>")
    log(f"検索ワード： {search_keyword}")
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()


    # 全件数からページ数を計算
    total_result_number = int(driver.find_element_by_xpath("//em").text)

    # 全件数が50の倍数以外は商プラス１ページ
    if total_result_number % 50 == 0:
      total_page_number = total_result_number // 50
    else:
      total_page_number = total_result_number // 50 + 1

    log(f"検索対象ページ数：{total_page_number}")


    name_list = []
    target_list = []
    workplace_list  = []

    # ページ数分繰り返し
    for i in range(total_page_number):
      # 検索結果の会社名を取得
      name_list_per_page = driver.find_elements_by_class_name("cassetteRecruit__name")
      for name in name_list_per_page:
        name_list.append(name.text)

      # 検索結果の初年度年収を取得
      target_list_per_page = driver.find_elements_by_xpath("//th[@class='tableCondition__head'][contains(text(), '対象となる方')]/following-sibling::td")
      for target in target_list_per_page:
        target_list.append(target.text)
          
      # 検索結果の給与を取得
      workplace_list_per_page = driver.find_elements_by_xpath("//th[@class='tableCondition__head'][contains(text(), '勤務地')]/following-sibling::td")
      for workplace in workplace_list_per_page:
        workplace_list.append(workplace.text)

      if i == total_page_number - 1:
        log("最終ページ終了")
        break
      
      next_btn = driver.find_element_by_xpath("//li[@class='pager__item--active']/following-sibling::li/a")
      driver.execute_script('arguments[0].click();', next_btn)
      time.sleep(5)

    # CSVへ出力
    try:
      CSV_PATH = "./{search_keyword}_{datetime}.csv"
      now = datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')
      df = pd.DataFrame({"会社名":name_list,
                        "初年度年収":target_list,
                        "給与":workplace_list})
      df.to_csv(CSV_PATH.format(search_keyword=search_keyword,datetime=now), encoding="utf-8-sig")
    except:
      log("CSVファイルに変換することができませんでした。")




# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()