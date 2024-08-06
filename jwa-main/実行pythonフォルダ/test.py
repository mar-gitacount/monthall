import requests
from bs4 import BeautifulSoup
login_url = 'https://mypage.jwa1.jp/login'  # ログインページのURL
username = 'k-umemoto@glorious-e.com'
password = '93RWIU6V'

# ログイン情報を含むデータ
login_data = {
    'username': username,
    'password': password
}

# ログインに必要なヘッダー
headers = {
    'User-Agent': 'Your User Agent',
    'Referer': 'https://mypage.jwa1.jp/login'
}
# セッションの開始
session = requests.Session()

# ログインリクエストの送信
response = requests.post(login_url, data=login_data, headers=headers)

# レスポンスの解析
if response.ok:
    print("ログイン成功")
    # ここでセッション情報やトークンを取得して利用する
        # ログイン後のページにアクセス
    target_url = 'https://mypage.jwa1.jp/?page=2'
    target_response = session.get(target_url)

    # ページのHTMLを取得
    target_html = target_response.text
    
  
    
    # BeautifulSoupなどを使用してHTMLを解析
    soup = BeautifulSoup(target_html, 'html.parser')


    # 例: ページのタイトルを取得
    title = soup.title.text
    print(f"タイトル: {title}")

    # body要素を取得
    body_element = soup.body
        # body要素のテキストを表示
    if body_element:
        print("body要素のテキスト:")
        print(body_element.get_text())
    else:
        print("body要素が見つかりませんでした。")
    # ここで必要な処理を行う


else:
    print("ログイン失敗")
    print(response.text)
