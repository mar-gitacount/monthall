from bs4 import BeautifulSoup
import re
import csv
import os

# 新しいCSVファイルのパス
csv_file_path = '新しいファイル.csv'

# CSVファイルを書き込みモードで開く
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    # CSVライターを作成
    csv_writer = csv.writer(csv_file)

    # ヘッダ行を書き込む
    header_row = [
        '会場', '開催日', '箱番号', '番号', 'レーン名', '品名', 'ブランド名', '素材', '脇石・AT・サイズ',
        '重量', '品番', 'ランク', 'スタート価格', '予想時刻', 'オークション結果', '落札価格'
    ]
    csv_writer.writerow(header_row)
    current_directory = os.getcwd()
    # HTMLファイルのパス
    # html_file_path = r'C:\Users\01794\Desktop\仕事でつかうやつ\jwa\test.html'
    html_relative_path = 'test.html'
    # html_file_path =  r'C:\Users\01794\Desktop\仕事でつかうやつ\jwa\test.html'
    # HTMLファイルの絶対パスを生成
    html_file_path = os.path.join(current_directory, html_relative_path)
    # 表示
    print("HTMLファイルの絶対パス:", html_file_path)
    try:
        # HTMLファイルを読み込む
        with open(html_file_path, 'r', encoding='utf-8') as file:
            # BeautifulSoupを使用してHTMLを解析
            soup = BeautifulSoup(file, 'html.parser')

            # クラスが "st-lists" の要素を取得してループ処理
            st_lists_elements = soup.find_all(class_='st-lists')


            # 商品詳細が始まる合図の文字列
            product_detail_indicator = "商品詳細"
            data_rows = []
            data_rows_child = []
            # lot_pattern = re.compile(r'Lot\. (\d+-\d+)')
            lot_pattern = re.compile(r'LOT\s*\.?\s*(\d+-\d+)', re.IGNORECASE)
            # テキストから金額を抽出
            price_pattern = re.compile(r'¥ ([\d,]+(\.\d+)?)')
            for st_lists_element in st_lists_elements:
                # ここでst_lists_elementに対して必要な処理を行う
                # print(st_lists_element.text)
                input_text = st_lists_element.text
                text =  input_text.splitlines()
                # print(test)
                # print(str.splitlines())
                 # ループ処理
                for item in text:
                    print(item)
                    LOT_match_result = lot_pattern.search(item)
                    PRICE_match_result = price_pattern.search(item)
                    print("------------")
                    if  LOT_match_result:
                        print(item)
                        data_rows_child.append(item)
                    if PRICE_match_result:
                        print(item)
                    if product_detail_indicator in item:
                        # print("商品詳細！！！！！！！！！！！！！！！！")
                        data_rows.append(data_rows_child)
                        # CSVライターを作成
                        csv_writer = csv.writer(csv_file)
                        # 新しい行を追加
                        csv_writer.writerow(data_rows_child)
                        data_rows_child.clear()
                        continue
                        # print(item)
                csv_writer.writerow(data_rows)

                # price_pattern = re.compile(r'落札価格\n\s*¥ ([\d,]+)')
                numeric_pattern = re.compile(r'([\d,]+\(\d+\.\d+\))')
                # テキストからロットナンバーを情報を抽出
                lots = lot_pattern.findall(input_text)


                price_elements = price_pattern.findall(input_text)

                # 不成立の文字列があるか確認する正規表現パターン
                not_successful_pattern = re.compile(r'不成立')

                # テキストから品番を抽出
                sinaban_pattern = re.compile(r'型番 (\d+\w*) シリーズ')
                sinaban_elements = sinaban_pattern.findall(input_text)

                # sinaban_elementsが空の場合、デフォルト値['N/A']を設定
                sinaban_elements = sinaban_elements or ['N/A']

                fuzokuhinandbikou_pattern = re.compile(r'付属品(.*?)備考')
                fuzokuhinandbikou_elements = fuzokuhinandbikou_pattern.findall(input_text)

                alphabetnumber_pattern = re.compile(r'備考 デイトジャスト (\w+番)')
                alphabetnumber_elements = alphabetnumber_pattern.findall(input_text)

                # 各Lotの情報を表示
                for j, lot in enumerate(lots):
                    # print(f'Lot {lot}')
                    # 落札価格を表示
                    if j < len(price_elements):
                        price_element = price_elements[j][0]
                        # 不成立の文字列が含まれているか確認
                        not_successful_match = not_successful_pattern.search(price_element)

                        if not_successful_match:
                            print('不成立')
                            print(f'不成立が含まれる要素番号: {j}')
                            price_element = 'N/A'  # 不成立の場合は 'N/A' を設定
                        else:
                            # 不成立が含まれていない場合、金額を表示
                            print(f'落札価格: {price_element}')
                    else:
                        price_element = 'N/A'
                        print(f'エラー: 落札価格のデータがありません（要素番号: {j}）')

                    # 品番を表示
                    if j < len(sinaban_elements):
                        jointitem = alphabetnumber_elements[j] + fuzokuhinandbikou_elements[j]
                        data_rows_child = [
                            'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',
                            'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', price_element
                        ]
                        data_rows_child[-6] = sinaban_elements[j]
                        csv_writer.writerow(data_rows_child)

    except FileNotFoundError:
        print(f'File not found: {html_file_path}')
    except Exception as e:
        print(f'An error occurred: {e}')
