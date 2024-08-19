import os
import json
import re
import sys
from datetime import datetime




class JosnDataGet:
    def __init__(self, jsonfile, datasection=None, data=None):
        self.jsonfile = jsonfile
        self.datasection = datasection
        self.data = data

    # JSONファイルを開くメソッド
    def jsonfileopen(self):
        with open(self.jsonfile, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def is_valid_date(self,date_string):
        pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        return bool(pattern.match(date_string))

    def check_key_in_master(self, key, checkdatas="master"):
        with open(self.jsonfile, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            master_data = json_data.get(checkdatas, {})
        for item_key, item_value in master_data.items():
            if item_key == key:
                return item_value
        # return key in master_data


# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)
# 一つ上のディレクトリを参照する
one_levels_up = os.path.abspath(os.path.join(current_dir, '..'))
# データを入稿するスクリプトを読み込む。
# sys.path に一つ上の階層を追加
sys.path.append(one_levels_up)
from whochedata_sqlite_data_insert import WhocheSqliteDataInsert
# db
db_file = os.path.join(one_levels_up,"bucherer.db")
# dbインスタンス
whocequeryinstance = WhocheSqliteDataInsert(db_file)
items = whocequeryinstance.tablesdateill
watch_item_instance = items["watch_item"]

# 日付事にループ→item抽出→masterを検索→一致したら日付と一致したデータをsqliteへ入稿する。



# JSONファイルのパス
BuchererMainDatasjson = "Buchererjson/BuchererMainDatas.json"
jsonfile = BuchererMainDatasjson  # JSONファイルのパス

# クラスのインスタンスを作成し、JSONファイルを開く
json_data_getter = JosnDataGet(jsonfile)
json_data_getter.jsonfileopen()

# 読み込まれたデータを出力
# print(json_data_getter.data)

jsondatas = json_data_getter.data

for section_name , section_data in jsondatas.items():
    date_valid = json_data_getter.is_valid_date(section_name)
    # データを検索する
    if date_valid:
        for key ,value in section_data.items():
            # masterでデータ詳細を確認する
            print(f"Section: {section_name}→{key}: {value}")
            # key = TOURNEAUのID value = 値段
            # dbのidをTOUNEAUにする。
            # 時計のデータ詳細。
            key_dataill = json_data_getter.check_key_in_master(key)
            print(key_dataill)
            if not key_dataill:
                continue
            if not value:
                continue 
            # year =key_dataill.get('year')
            # ID
            insert_id = key
            ref = key_dataill['ref']
             # 年
            year = key_dataill['year']
            # モデル
            model = key_dataill['model']
            # サイズ
            size = key_dataill['size']
            # ブレスレット
            bracelet = key_dataill['bracelet']
            # ダイアル
            dial = key_dataill['dial']
            # URL
            url = key_dataill['url']
            # 会社名
            company_name = 'TOURNEAU'
            # 値
            print(value)
            price = value['price']

            if '$' in price:
                price = price.replace("$","")
          
            # price = int(value['price'].replace(',',''))
            price = int(price.replace(',',''))
            
            # section_name = 日付
            # 日付をdbに保存できる形式にする
            date_obj = datetime.strptime(section_name, '%Y-%m-%d')
            # 日付
            formatted_date = date_obj.strftime('%Y/%m')
            
            watch_item_instance.insert_data([insert_id,ref,year,model,size,bracelet,dial,url,company_name,price,formatted_date,"その他",""])



   
    