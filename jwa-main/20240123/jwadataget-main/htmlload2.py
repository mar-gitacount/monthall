from bs4 import BeautifulSoup
import os
import re
import csv

def read_csv_and_replace_empty_with_none(file_path):
    data = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # print(row)
            # for r in row:
            #     print(r)
            #     new_row = [cell if cell.strip() != '' else None for cell in r]
            #     data.append(new_row)
            new_row = [cell if cell.strip() != '' else None for cell in row]
            data.append(new_row)
        print(data)
    return data
# htmlにあるかぶりの商品をチェックする。
def lot_number_check_array (array,lot):
    for item in array:
        # print(item)
        if(item == lot):
            print(lot)
            print("データチェック")
            return True
    print("ループ回り切った")
    return False

def material_codes_get(num):
    # int型に変換する
    num = int(num)
    # 素材コード
    material_codes = {0:"SS",1:"SR",3:"SY",4:"SW",5:"RG",6:"PT",7:"その他",8:"YG",9:"WG"}
    material_code = material_codes.get(num)
    print (f'{num}の{material_code}コード')
    return material_code



def extract_type_number(data_string):
    # 正規表現を使用して末尾から最初の数字を抽出
    index = 1
    for item in data_string:
        last_digit = data_string.strip()[-index]
        print(last_digit)
        if last_digit.isdecimal():
            material_code = material_codes_get(last_digit)
            print("正しい数字")
            return material_code
        else:
            index += 1
    # match = re.search(r'(\d+)$', data_string[::-1])
    
    # if match:
    #     type_number_reversed = match.group(1)
    #     print(type_number_reversed)
    #     # 反転した文字列を元に戻す
    #     type_number = type_number_reversed[::-1]
    #     return type_number
    # else:
    #     return None

# html_file_path = r'C:\Users\01794\Desktop\仕事でつかうやつ\jwa\test.html'
current_directory = os.getcwd()
html_relative_path = 'test.html'
html_file_path = os.path.join(current_directory, html_relative_path)
lot_number_array = []
try:
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        st_lists_elements = soup.find_all(class_='st-lists')

        # 辞書型のリストを初期化
        data_list = []
        lot_range_pattern = re.compile(r'Lot\. (\d+)-(\d+)')
        # 末尾から数字を検索する正規表現
        last_digit_pattern = re.compile(r'(\d+)$')
        # 日付を取得する正規表現
        date_pattern = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')

        low_data_list=[None]*20
        csv_data_list=[]
        csv_data_list_index = 0
        Lot_number_flg = 0
        # 素材コード
        material_codes = {0:"SS",1:"SR",3:"SY",4:"SW",5:"RG",6:"PT",7:"その他",8:"YG",9:"WG"}
        # 要素ごとに処理
        for st_lists_element in st_lists_elements:
            # 新しいLotが始まる場合
            current_lot = {'Lot': st_lists_element.find('span', class_='lot').text.strip() if st_lists_element.find('span', class_='lot') else ''}
            input_text = st_lists_element.text
            text = input_text.splitlines()
            
            print(input_text)
            print(text)
            lot_range_pattern = re.compile(r'Lot\. (\d+)-(\d+)')
            
            for item in text:
                # matches = lot_range_pattern.findall(item)
                # print(item)
                #日付を取得する。
                date_matches = date_pattern.search(item)
                if date_matches:
                    low_data_list.insert(1,date_matches.group(0))

                lot_matches = lot_range_pattern.findall(item)
                # 商品詳細になった際に、次の項目に行く処理
                # if '商品詳細' in item:
                #     # print("商品詳細")
                #     csv_data_list.append(low_data_list)
                #     # print(csv_data_list)
                #     low_data_list=[]*16
                #     csv_data_list_index += 1
                # 配列を渡して、ロットナンバーを検索、無ければ実行、あればcontinue
                 # ロットナンバーを取得する
                if lot_matches:
                    # print(item[0])
                    for lot in lot_matches:
                        # ここでlotを関数にわたし、trueが返ってくればcontinue
                        print(f'{lot}番号')
                        # box_number = min(lot)
                        # branch_number = max(lot)
                        box_number = lot[0]
                        branch_number = lot[1]
                        # checkno = box_number+"-"+branch_number
                        # lot_number_array.append(checkno)
                        # datacheck = lot_number_check_array(lot_number_array,checkno)
                        # low_data_list.insert(3,box_number)
                        # low_data_list.insert(4,branch_number)
                        # if(datacheck):
                        #     break
                        # else:
                        low_data_list.insert(0,"東京エムジー時計")
                        low_data_list.insert(2,box_number)
                        low_data_list.insert(3,branch_number)
                        low_data_list.insert(4,"ー")
                        low_data_list.insert(5,"時計")
                        low_data_list.insert(6,"ROLEX")

                        
                        
                        # print(box_number)
                        # print(branch_number)
                        # if Lot_number_flg == 0:
                        #     low_data_list.append(box_number)
                        #     low_data_list.append(branch_number)
                        #     Lot_number_flg += 1
                        # # 次のループ確認フラグロットナンバーで確認する
                        # else:
                        #     # ループが終わってるはずなので、csvの配列に追加
                        #     csv_data_list.append(low_data_list)

                        #     low_data_list = []
                        #     low_data_list.append(box_number)
                        #     low_data_list.append(branch_number)

                            
                            # Lot_number_flg = 0
                            
                        # ここでフラグをたてて、二度目のロットナンバーなら、low_data_listを空にして、csv_data_listにプッシュする。
                if '不成立' in item :
                    low_data_list.insert(13,item)
                if ' ¥' in item :
                    # print(f'{item}は金額です')
                    price = item.replace(" ¥","")
                    low_data_list.insert(13,"落札")
                    low_data_list.insert(14,price)
                if 'ブランド' in item:
                    # 正規表現を使用して型番を抽出
                    silealnum_match = re.search(r'型番 (\d+)', item)
                    # アルファベット
                    # alhpabetnum_matches = re.findall(r'\b[A-Za-z]+\d番', item)
                    # 正規表現を使用して「付属品」から「備考」の前までを抽出
                    fuzokuhin_matches = re.search(r'付属品(.*?)備考(.*?)', item)
                    # 抽出した部分文字列
                    fuzokuhin_result = fuzokuhin_matches.group(1).strip() if fuzokuhin_matches else None
                    print(f'付属品{fuzokuhin_result}')

                    
                    bikou_matches = re.findall(r'備考(.*?)',item)
                    # bikou_result = bikou_matches.group(1).strip() if fuzokuhin_matches else None
                    # bikou_result = re.sub(r'^備考\s*', '', item)
                    bikou_result = re.sub(r'^.*備考\s*', '', item)
                    number_removed = re.sub(r'(\S+)番', '', bikou_result)
                    number_removed = number_removed.replace("本日レート","")
                    print(f'備考だお{number_removed}備考だお！')

                    # 以下アルファベット番号がない場合がある。
                    alhpabetnum_matches = re.findall(r'(\S+)番', item)
                    if (len(alhpabetnum_matches))<2:
                        # print("型番なし")
                        fuzokuhin_result = fuzokuhin_result.replace("\u3000"," ")
                        low_data_list.insert(10,fuzokuhin_result)
                    else:
                        # print(f'数字と番号は{alhpabetnum_matches}')
                        # print(fuzokuhin_result)
                        # 上記変数を合体させる、配列に追加する。
                        fuzokuhin_result = fuzokuhin_result.replace("\u3000"," ")
                        low_data_list.insert(10,alhpabetnum_matches[1]+"番"+" "+fuzokuhin_result+number_removed)

                    if silealnum_match:
                        type_number = silealnum_match.group(1)

                        # print(f'型番: {type_number}')
                        low_data_list.insert(9,type_number)
                        # 素材コード
                        low_data_list.insert(7,extract_type_number(type_number))
                        # Z番抽出
                        # print(f'素材コードは{extract_type_number(type_number)}')
                    else:
                        low_data_list.insert(9,"")
                        # 素材コード
                        low_data_list.insert(7,"")
                        print('型番が見つかりませんでした。')
                    # if alhpabetnum_matches:
                    low_data_list = [None if element == '' else element for element in low_data_list]
                    print(f'{len(low_data_list)}配列数')
                    csv_data_list.append(low_data_list)
                    # print(csv_data_list)
                    low_data_list=[None]*20
                    csv_data_list_index += 1

                    # print(item)
               
            
            # print(text)
            # print(csv_data_list)
            print("--------------")
          
            
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
        # print(csv_data_list)
        # 結果の表示
        for data in data_list:
            print(data)
    # print(csv_data_list)
    # csvに書き込み
    with open('output.csv', 'w', newline='',encoding='utf-8') as csvfile:
        # CSVライターを作成
        csvwriter = csv.writer(csvfile)
        # データをCSVファイルに書き込む
        csvwriter.writerows(csv_data_list)
    



    # current_directory = os.getcwd()
    # csv_relative_path = 'output.csv'
    # csv_file_path = os.path.join(current_directory, csv_relative_path)
    # print(f'{csv_file_path}はcsvのファイルパス')
    # nonereplaceresult = read_csv_and_replace_empty_with_none(csv_file_path)
except FileNotFoundError:
    print(f'File not found: {html_file_path}')
except Exception as e:
    print(f'An error occurred: {e}')
