from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

# ChromeDriverを自動でインストール
chromedriver_autoinstaller.install()

# ログイン情報
username = 'k-umemoto@glorious-e.com'
password = '93RWIU6V'

# WebDriverの設定
options = webdriver.ChromeOptions()
options.headless = False  # ブラウザを表示する場合はFalseにする

# ChromeDriverのパスを取得
chromedriver_path = chromedriver_autoinstaller.install()

# セッションの開始
driver = webdriver.Chrome(service=ChromeService(), options=options)

# ログインページにアクセス
driver.get('https://mypage.jwa1.jp/login')

# ログイン
driver.find_element_by_name('username').send_keys(username)
driver.find_element_by_name('password').send_keys(password)
driver.find_element_by_name('login_button').click()

# ログイン後のページにアクセス
driver.get('https://mypage.jwa1.jp/')

# ページのHTMLを取得
target_html = driver.page_source

# BeautifulSoupを使用してHTMLを解析
soup = BeautifulSoup(target_html, 'html.parser')

# body要素を取得
body_element = soup.body

# body要素のテキストを表示
if body_element:
    print("body要素のテキスト:")
    print(body_element.get_text())
else:
    print("body要素が見つかりませんでした。")

# ブラウザを閉じる
driver.quit()
