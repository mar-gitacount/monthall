from bs4 import BeautifulSoup

html_file_path = r'C:\Users\01794\Desktop\仕事でつかうやつ\jwa\test.html'

try:
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        st_lists_elements = soup.find_all(class_='st-lists')

        # 辞書型のリストを初期化
        data_list = []

        # 要素ごとに処理
        for st_lists_element in st_lists_elements:
            # 新しいLotが始まる場合
            current_lot = {'Lot': st_lists_element.find('span', class_='lot').text.strip() if st_lists_element.find('span', class_='lot') else ''}
            data_list.append(current_lot)

            # 落札価格を取得
            current_lot['落札価格'] = st_lists_element.find('div', class_='price').text.strip() if st_lists_element.find('div', class_='price') else ''

            # 商品詳細が始まる場合
            current_item = {}
            current_lot['商品詳細'] = current_item

            # 商品詳細内の情報を取得
            details = st_lists_element.find('div', class_='details')
            if details:
                for detail in details.find_all('div', class_='detail'):
                    key_element, value_element = detail.find_all('div')
                    key = key_element.text.strip() if key_element else ''
                    value = value_element.text.strip() if value_element else ''
                    current_item[key] = value

        # 結果の表示
        for data in data_list:
            print(data)

except FileNotFoundError:
    print(f'File not found: {html_file_path}')
except Exception as e:
    print(f'An error occurred: {e}')
