import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd

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
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def main():
    search_keyword = "高収入"
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

    print(total_page_number)

    for i in range(total_page_number):
      # ページ終了まで繰り返し取得
      exp_name_list = []
      # 検索結果の会社名を取得
      name_list = driver.find_elements_by_class_name("cassetteRecruit__name")

      # 1ページ分繰り返し
      print(len(name_list))
      for name in name_list:
          exp_name_list.append(name.text)
          print(name.text)

      # 検索結果の初年度年収を取得
      first_income_list = driver.find_elements_by_xpath("//th[@class='tableCondition__head'][contains(text(), '初年度年収')]/following-sibling::td")

      print(len(first_income_list))
      for first_income in first_income_list:
        print(first_income.text)
          
      # 検索結果の給与を取得
      income_list = driver.find_elements_by_xpath("//th[@class='tableCondition__head'][contains(text(), '給与')]/following-sibling::td")

      print(len(income_list))
      for income in income_list:
        print(income.text)
      
      if i == total_page_number - 1:
        break
      
      next_btn = driver.find_element_by_xpath("//li[@class='pager__item--active']/following-sibling::li/a")
      driver.execute_script('arguments[0].click();', next_btn)
      time.sleep(5)



# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()