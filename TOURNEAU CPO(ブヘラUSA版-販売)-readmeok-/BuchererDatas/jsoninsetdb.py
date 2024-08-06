import os
import json
import sqlite3
from sqlite_data_insert import SQLiteDataInsert
from datetime import datetime
import re

file_path = "BuchererMainDatas.json"
def connect_db():
    return sqlite3.connect('TOURNEAU.db')

# インスタンスにdb名、テーブル名、フィールド名を入れ込む。
# db名
dbname = 'TOURNEAU.db'
# テーブル名
table_name = 'watch_item'
# DBのフィールド名を設定する。
fields = ['bucherer_watch_id','year','model_name','size','ref','bracelet','dial','url']

# DB名、テーブル名、フィールド名を設定したインスタンスを作成する。
watch_item_insert_instance = SQLiteDataInsert(dbname,table_name,fields)

# 週テーブル
weekly_table_name = 'weekly_reports'
# 週フィールド名
weekly_table_fields = ['weekdate','ranking','price','bucherer_watch_id']


# 週レポート
weekly_report_inset_instance = SQLiteDataInsert(dbname,weekly_table_name,weekly_table_fields)

# データを設定する
# values = [1,2022, "Model 1", "REF123", "Bracelet 1", "Dial 1", "test.com"]
# # データ入稿する。
# watch_item_insert_instance.insert_data(values)
# watch_item_insert_instance.close_connection()
# inserter = SQLiteDataInsert('bucherer.db')
# # データを挿入
# inserter.insert_watch_item("watch_item",1, 2022, "Model 1", "REF123", "Bracelet 1", "Dial 1", "example.com")

# # 接続を閉じる
# inserter.close_connection()


conn = connect_db()
c = conn.cursor()
# JSONファイルを読み込む
with open(file_path, "r") as json_file:
    data = json.load(json_file)

# data["main"]
# ここでウィークリーチェックする
for item, daysdata in data.items():
    # print(daysdata)
    # 日付確認する
   
    try:
        # ここで正常に動けばそれをdbにinsertする
        # print(item)
        # print(daysdata)
        date_obj = datetime.strptime(item, "%Y-%m-%d")
        # daysdata = data[item]
        # 日付で確認してcontinue

        for i in daysdata:
             # 以下形式でデータを入れ込む        
             itemdict = daysdata[i]
             if not itemdict:
                 continue
             
             
             bucherer_watch_id = i

             count = weekly_report_inset_instance.datacountcheck(item,['weekdate'])

             price = itemdict['price']
             price_pattern = r'\d{1,3}(?:,\d{3})*'
             pricematch = re.search(price_pattern,price)
             if pricematch:
                 price = price.replace(",","")
            #  値段
             price = int(price)
            #  日付
             insert_date = date_obj.strftime('%Y/%m/%d')
            #  データをインサートする
             print(f"{price}で値段をチェックする")
             print(f"{i}はシリアルナンバー{itemdict}で値チェック{insert_date}は日付")
            #  weekly_table_fields = ['weekdate','ranking','price','bucherer_watch_id']
             
             check_fields = ["weekdate","bucherer_watch_id"]
             check_values = [insert_date,i]
            #  日付テーブルにデータを入稿する。
             count = weekly_report_inset_instance.datacountcheck(check_values,check_fields)
             if not count > 0:
                 insert_values = [insert_date,"0",price,bucherer_watch_id]
                 print(insert_values)
                 weekly_report_inset_instance.insert_data(insert_values)
             
            #  print(itemdict["price"])

             print(f"{type(i)}を取得する")
             if isinstance(i ,dict):
                  insert_date = date_obj.strftime('%Y/%m/%d')
                  try:
                      search = str(i)
                      print(i.get("price"))
                      price = i.get("price")
                      if price is None:
                          print("値段がない")
                      print(item,"値段チェック")
                      print(item[search["price"]])
                  except TypeError:
                      print(f"{date_obj}値段なし")
       
    except ValueError as e:
         print(f"無効な日付形式です{e}")
    # print(item)
    
    # 日付分岐して、trueならweekly_reportsにデータを入れ込む。

    print("jsonデータチェック")

masterdata = data["master"]
# masterデータをループする。
for item in masterdata:
    datas = masterdata[item]
    # データ入稿する。
    # print(item)
    # idでアイテム数をチェックする。
    conut = watch_item_insert_instance.datacountcheck(item,['bucherer_watch_id'])
    if conut > 0:
        continue

    values = [item, datas["year"], datas["model"], datas["ref"], datas["size"], datas["bracelet"], datas["dial"], datas["url"]]
    c.execute('''INSERT OR REPLACE INTO watch_item(bucherer_watch_id, year, model_name, size ,ref, bracelet, dial, url) VALUES (?, ?, ?, ?, ?, ?, ?,?)''', (item, datas["year"], datas["model"], datas["ref"], datas["size"], datas["bracelet"], datas["dial"], datas["url"]))

    conn.commit()
    # print("------")
# # 読み込んだデータを表示する
# # print(data["master"])