from selenium import webdriver
import os
import json
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
# useBucheradataget.py
# ここに処理をかく
# !jsonファイルのパス
BuchererMainDatasjson = "Buchererjson/BuchererMainDatas.json"


# 新しいデータ作成処理
# 現在の日付と時刻を取得
current_datetime = datetime.now()
# 現在の日付を取得（年-月-日）
current_date = current_datetime.date()
# 現在の時刻を取得（時:分:秒.マイクロ秒）
current_time = current_datetime.time()
# 取得日をjsonファイルデータ名にする
json_datagetnow = str(current_date)

def main():
    # jsonファイルに存在するかどうか確認する
    def check_key_in_master(json_file, key, checkdatas="master"):
        with open(json_file, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            master_data = json_data.get(checkdatas, {})
            return key in master_data
        
    # jsonファイルに追加する。
    def add_data_to_master(json_file, key, data, checkdatas="master"):
       with open(json_file, "r+", encoding="utf-8") as file:
        json_data = json.load(file)
        master_data = json_data.setdefault(checkdatas, {})
        if key not in master_data:
            master_data[key] = data
            file.seek(0)
            json.dump(json_data, file, indent=4)
            print(f'キー "{key}" のデータが "{checkdatas}" に追加されました。')
        else:
            print(f'キー "{key}" は既に "{checkdatas}" 内に存在します。')

    # 文字列が返ってくる
    def sizeandyearextraction(text):
        if text is not None:
            print("アイテムあるよ")
            parts = text.split(", ")
            # 正規表現する。
            year = re.search(r'\b\d{4}\b', text)
            size = re.search(r'\b\d+\s*mm\b', text)
            if year:
                 print(year.group(),"年代を抽出")
                 year = year.group()
            else:
                print(year,"年代はない")
                year = "-"
            if size:
                size = size.group()
            else:
                size = "-"
            return {"size":size,"year":year}
        else:
            return {"size":"-","year":"-"}
    # useBucheradataget.pyを実行したいコードをここに記述します
    # webdriverを実装する。
    # WebDriverを初期化
    # 日付データを入れる処理
    add_data_to_master( 
    BuchererMainDatasjson, key=json_datagetnow, data={}, checkdatas="date")
    #! とりあえず既存のやり方であるJSON形式でのデータ格納を実装して、あとでDB格納する。
    start = 0
    
    pageend = 56
    # 17ずつ加算される。
    sz = 17
    driver = webdriver.Chrome()
    
    for i in range(pageend):
        url = f"https://www.tourneau.com/rolex-certified-pre-owned-watches/?start={start}&sz=17"
        secondacccessurl = "https://www.tourneau.com/"
    #    https://www.tourneau.com/rolex-certified-pre-owned-watches/?start=0=0&sz=17
    #    https://www.tourneau.com/rolex-certified-pre-owned-watches/?start=17=0&sz=17
        print(url)
        start += 17
        # time.sleep(5)
        # Webページに移動
        driver.get(url)
        first_page_get = driver.page_source

        soup = BeautifulSoup(first_page_get,"html.parser")
        
        # print(first_page_get)
        # メインカラム
        MainColumn = soup.find("div",id = "main")
        # 各時計データ
        try:
            WatchItem = MainColumn.find_all("div",class_="watch-grid__col")
        except Exception as e:
            print(url,"←エラーページ")
        # 各時計アイテム
        for item in WatchItem:
            if item is not None:
                # itemsoup = BeautifulSoup(item,"html.parser")
                geturl = item.find_all("a")
                # アクセスするURL
                getaccessurl = item.find("a",class_="rolex-tile--hover").get("href")
                # ?URL
                dateilaccessurl = secondacccessurl + getaccessurl
                # 各アイテム詳細にアクセスしている。
                driver.get(dateilaccessurl)
                datail_page_get = driver.page_source
                datail_page_get_soup = BeautifulSoup(datail_page_get,"html.parser")
                try:
                    h_one = datail_page_get_soup.find("h1")
                   # ?2モデル名
                    model = h_one.find("span",class_="medium-title").text.strip()
                except Exception as e:
                     model = ""
                # ?詳細ページの左側
                left_item = datail_page_get_soup.find("div",class_="watch-specs-left")
                # ?詳細ページの右側
                right_item = datail_page_get_soup.find("div",class_="watch-specs-right")
            
                #? 1.アイテムナンバー
                item_number = left_item.find("div",text="Item Number").find_next_sibling("div", class_="description").text.strip()
                
                # ?8.ブレスレット
                # ?ダイアル
                try:
                    dial = right_item.find("div",text="Dial").find_next_sibling("div", class_="description").text.strip()
                except Exception as e:
                    dial = ""
                # ? 6.リファレンスナンバー
                ref_item = left_item.find("div", text="Reference").find_next_sibling("div", class_="description").text.strip()
                print(ref_item,"←はリファレンスナンバー")
                print(item_number,"←はアイテムナンバー")
                print(dial,"←はダイアル")
                getitem = item.find("div",class_="rolex-tile__content")
                # アイテム名
                itemname = item.find_all("p")
              
                # 年代、mmを取得する
                items_without_class = [p for p in item.find_all("p") if not p.get("class")]
                texts = items_without_class[0].text.strip() if items_without_class else None
                # 辞書形式で年代とサイズが返ってくる。何もない場合はどちらも空の文字列が返ってくるので、そのままテキストとして利用する。
                sizeandyeardata = sizeandyearextraction(texts)
                # ?3年代
                yeardata = sizeandyeardata["year"]
                # ?4サイズ
                sizedata = sizeandyeardata["size"]

                # 金額
                price = getitem.find("div",class_="product-price").find("span").text.strip()
               
                # 以下がfalseの場合、データを追加する。
                if not check_key_in_master(BuchererMainDatasjson,item_number):
                    print(f"{item_number}が存在しないため、masterデータに追加します。")
                    data_to_add ={
                    "model":model,
                    "year":yeardata,
                    "ref":ref_item,
                    "size":sizedata,
                    "bracelet":"",
                    "dial":dial,
                    "url":dateilaccessurl
                    }
                    add_data_to_master(
                        BuchererMainDatasjson,
                        data = data_to_add,
                        key = item_number,
                        checkdatas="master"
                    )
                else:
                    print(f"{item_number}がすでにmasterに存在します。追加処理はされませんでした。")

                # 実行日のデータを追加する。
                add_data_to_master(
                    BuchererMainDatasjson,
                    data={"price":price},
                    key=item_number,
                    checkdatas=json_datagetnow

                )
        # print(watchcol)

    print("メインを実行する")
    
    return "ブヘラのアメリカ版の確認!!"
# mainメソッドを呼び出す
if __name__ == "__main__":
    main()