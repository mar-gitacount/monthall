# サイズとリファレンすの値を逆にしたい
from whochedata_sqlite_data_insert import WhocheSqliteDataInsert
from sqlite_data_insert import SQLiteDataInsert
from datetime import datetime, timedelta
from openpyxl import Workbook, load_workbook
import os
from datetime import datetime
import jpholiday
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import math
from openpyxl.styles import PatternFill

def main():
    # インスタンスを作成する。
    db_file = "bucherer.db"
    # dbのファイルをわたす。
     # 再度インスタンスを作成する
    whocequeryinstance_watch_item_use = WhocheSqliteDataInsert(db_file)
    # テーブル一覧プロパティ
    watch_item_use_tablename = whocequeryinstance_watch_item_use.table_names
    watch_item_use_items = whocequeryinstance_watch_item_use.tablesdateill
    # print(watch_item_use_tablename)
    watch_items = watch_item_use_items['watch_item']
    wath_item = watch_items.dataget("test")


    for item in wath_item:
        print(f"アイテム→{item}")
        item[4],item[5] = item[5], item[4]
        # watch_items.excehngevalue(item[5],item[4],item[0])
        watch_items.insert_data(item)
    return
 

    # リファレンスを抽出する。実際はサイズが入っている。
    sizeitems = watch_item.dataget("ref")

    # サイズアイテムを削除する
    for refitem in refitems:
        # サイズテーブル参照する
        watch_item.datedelete("size",refitem)
    
    # サイズアイテムを入稿する。
    watch_item.fields =[]
    watch_item.fields.append("size")

    for sizeitem in sizeitems:
        watch_item.insert_data(sizeitem)

    # リファレンスアイテムを削除する
    for sizeitem in sizeitems:
        watch_item.datedelete("ref",sizeitem)
    watch_item.fields =[]
    watch_item.fields.append("ref")

    
    # リファレンスアイテムを入稿する
    for refitem in refitems:
        watch_item.insert_data(refitem)


    # リファレンスアイテムを削除する。

    # サイズアイテムを削除する。
    
    # print(watch_item_use_items['watch_item'])
    # 時計一覧のインスタンスを作成する。
    
    # bucherer_table_instance = watch_item_use_items["watch_item"]
    #  これを使う→before_date_price = bucherer_table_instance['weekly_reports'].serachitem([id,dates[0]],["bucherer_watch_id","weekdate"])


    #  insert_data(self,values):でsizeおよびrefを入れ替える。
    

    



if __name__ == "__main__":
    main()