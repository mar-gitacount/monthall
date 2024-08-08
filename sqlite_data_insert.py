# sqlite_data_insert.py

import sqlite3
from collections import defaultdict
class SQLiteDataInsert:
    def __init__(self, db_file,table_name,fields):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        # テーブル名
        self.table_name = table_name
        # フィールド名
        self.fields = fields
    

    # フィールドと検索値で結果を返すメソッド
    def serachitem(self,values,fields):
         print("値を検索する")
         
         placeholders = ', '.join(['?'] * (len(fields)))
         fields_str = ', '.join(self.fields)
        # 検索クエリの生成
         conditions = " AND ".join([f"{field} = ?" for field in fields])
         search_query = f"SELECT * FROM {self.table_name} WHERE ({conditions})"
         print(search_query)
       
         # データベースに接続してクエリを実行
         cursor = self.conn.cursor()
         cursor.execute(search_query, values)
         results = cursor.fetchall()
        #  self.conn.close()

         return results
    
    def close_connection(self):
         if self.conn:
            self.conn.close()
            self.conn = None


    # フィールドのなかの値の数を返す。
    def fieldcountAllcountcheck(self,):
         print(self.table_name,"テーブル名をチェックする")
        # self.cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        #  self.cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
         self.cursor.execute(f"SELECT MAX({self.fields[0]}) FROM {self.table_name}")
      
        # プライマリキーは一番目と想定して実装している。
         count = self.cursor.fetchall()[0][0]
         print(f"これがあやしい→{count}テーブル名{self.fields[0]}")
         testcount = count + 1
         print(f"{count}はもともとのカウント→は1足したやつ{testcount}")
         count += 1

         
         return count
        #  print(query)
    # データ一覧を閲覧
    def excehngevalue(self,new_size,new_ref,id):
        print(f"サイズ:{new_size} リファレンス:{new_ref} ID:{id}")
        #  self.conn.begin() 
        update_query = f"UPDATE watch_item SET size = ?, ref = ? WHERE bucherer_watch_id = ?"
        self.cursor.execute(update_query, (new_size, new_ref, id))
        # コミットして変更を確定させる。
        print("conn前")
        self.conn.commit()
        # query = f"INSERT OR REPLACE INTO {self.table_name} ({fields_str}) VALUES ({placeholders})"
    

         
    # field＝フィールド value=要素
    def dataget(self,field):
        placeholders = ', '.join(['?'] * (len(self.fields)))
        # idも取得しなければならない

        query = f"SELECT * FROM {self.table_name}"
        # query = f"SELECT {field} FROM {self.table_name}"
        self.cursor.execute(query)
        all_items = self.cursor.fetchall()
        cleansing_items = []
        for item in all_items:
             print(list(item))
             cleansing_items.append(list(item))
        return cleansing_items
    
    # アイテム名を指定して削除する。
    def datedelete(self,field,value):
        # query = f"DELETE FROM {self.table_name} WHERE {field} = ?"
        query = f"UPDATE {self.table_name} SET {field} = '' WHERE {field} = ?"
        self.cursor.execute(query, (value,))
        self.conn.commit()
         
    # データ数を確認。
    def datacountcheck(self, value, field):
        #  フィールドを連結させる
        # チェックする値が一つ以上
         if len(field) > 1:
            #   all_field_query = " AND ".join([f"{f}" for f in field[:-1]])
              all_field_query = " AND ".join([f"{f} = ?" for f in field])

              query = f"""SELECT COUNT(*) FROM {self.table_name} WHERE {all_field_query}"""
                # バインドする値をリストに格納
              
            #   values = tuple([value] * len(field[:-1]))
              print("クエリ→",query)
              print(field)
              print(value,"フィールドが1以上の時にはいるとこ")
              self.cursor.execute(query, value)
         else:
              print("フィールドが一つ",value)
              print(field)
              query = f"SELECT COUNT(*) FROM {self.table_name} WHERE {field[0]} = ?"
              self.cursor.execute(query, (value,))
        #  query = f"SELECT MAX({primary_key_field}) FROM {self.table_name}"
         
         count = self.cursor.fetchone()[0]
         return count > 0

    def groupby(self,groupcolomn="test"):
        #  query = "SELECT name FROM sqlite_master WHERE type='table'"
        # SELECT 表示させるカラム名 FROM テーブル名 GROUP BY グループ化するカラム名;
        #  query = f"""SELECT COUNT(*) FROM {self.table_name} WHERE {all_field_query}"""
        # query = f"SELECT * FROM watch_item GROUP BY ref"
        # query = "SELECT DISTINCT ref, * FROM watch_item"
    #    query = "SELECT * FROM watch_item"
       query = "SELECT * FROM watch_item ORDER BY ref"
       return_All_array = []
       self.cursor.execute(query)
       rows = self.cursor.fetchall()
       print("グループ関数に入ってる")
       # データをリファレンス番号でグループ化するための辞書
       grouped_data = defaultdict(list)
       # データをリファレンスごとにグループ化
       # データをリファレンス番号でグループ化
    #    リファレンスナンバー
       diffcheckitem = ""
       company_dict = {}
       company_dictindex = 1
       insert_data = {}
       header = ["リファレンス","年代","モデル名","サイズ","ブレスレット","ダイアル","値段","その他","日付","URL"]
       headerlen = len(header) - 1 
       for item in rows:
            ref_number = item[1]  # リファレンス番号はタプルの2番目の要素に格納されている
            # print(item)
            item_array = list(item)
            # print(item_array)
            # item_array[0]を比べる。
            # print(item_array,"元配列")
            # 会社判定
            if not item_array[8] in company_dict:
                # before_dict[item[8]] = valuenum 
                # 各会社の列番号をいれる。
                # item_array[8]は会社名
                # 会社名を辞書入れ込む
                company_dict[item_array[8]] = company_dictindex
                # 中古値段があるかどうか
                if item_array[12]:
                    company_dictindex += 1
                    #会社の辞書配列に中古入れ込む
                    useprice_with_companiname = item_array[8] + "(中古)"
                    # 中古列追加する。
                    company_dict[useprice_with_companiname] = company_dictindex
                    
                    
                company_dictindex += 1
            # 二回目以降の処理、会社違い
            # ここに中古値段の処理を入れ込む？
            if item_array[1] in diffcheckitem:
                append_array = [""] * 50
                # 値段の列を辞書型より抽出する。
                print(company_dict)
                price_column = headerlen + company_dict[item_array[8]]
                print(price_column,"値段の場所")
                print(company_dict[item_array[8]])
                append_array[0] = item_array[1]
                append_array[1] = item_array[2]
                append_array[2] = item_array[3]
                append_array[3] = item_array[4]
                append_array[4] = item_array[5]
                append_array[5] = item_array[6]              
                append_array[7] = item_array[11]          
                # 日付
                append_array[8] = item_array[10]
                 # URL
                append_array[9] = item_array[7]
                print(item_array[9],"値段")
                append_array[price_column] = item_array[9]
                # 中古の値段
                if item_array[12]:
                    # 通常の値段のとなりにいれる
                    use_price_column  = price_column + 1
                    append_array[use_price_column] = item_array[12]
                # 未使用
                if item_array[13]:
                    unuse_price_column = price_column + 2
                    append_array[unuse_price_column] = item_array[13]
                # 辞書型に配列を追加する。
                insert_data[item_array[1]].append(append_array)
                return_All_array.append(append_array)
                # print(f"{append_array}は配列{item_array[1]}はアイテムナンバー　前の番号と同じ")
                # print("前の番号と同じ")
                print("-------------------")
                #前の番号と同じなので、値段以外の項目はいらない。 
            # リファレンスがおなじかつ会社違い→最後の配列を取得する。
            # 以下判定分は使われていないぽいが怖いのでさわらない
            elif item_array[1] in diffcheckitem and not item_array[8] in company_dict:
                # 会社を追加する。これを参考に、値段の列を設定する。
                append_array[2] = "会社を追加する。これを参考に、値段の列を設定する。"
                company_dict[item_array[8]] = company_dictindex
                # →値段item_array[9]            
                print("同アイテム違う会社")
                #company_dictindex ←これが列番号                                  
            else:      
                # 初めての番号なので、すべての項目を配列に入れ込む。
                diffcheckitem = item_array[1]        
                append_array = [""] * 50
                # 0番目と7番目の要素を削除して新しい配列を作成
                # 会社の名前で列番号を検索する。
                print(item_array,"アイテム一覧")
                print(item_array[9],"アイテム値段")


                print(company_dict)
                price_column = headerlen + company_dict[item_array[8]]
                print(price_column)
                # append_array = [it for i, it in enumerate(item_array) if i not in [0, 8]]
                # リファレンスナンバー
                append_array[0] = item_array[1]
                # 年代
                append_array[1] = item_array[2]
                # モデル名
                append_array[2] = item_array[3]
                # 年代
                append_array[3] = item_array[4]
                # ブレスレット
                append_array[4] = item_array[5]
                # ダイアル
                append_array[5] = item_array[6]
                # その他
                append_array[7] = item_array[11]
                # 日付
                append_array[8] = item_array[10]
                # URL
                append_array[9] = item_array[7]

                # 値段各種
                append_array[price_column] = item_array[9]
                # 中古値段判定
                
                if item_array[12]:
                    use_price_column  = price_column + 1    
                    append_array[use_price_column] = item_array[12]
                
                # 未使用の値段
                if item_array[13]:
                    unuse_price_column = price_column + 2
                    append_array[unuse_price_column] = item_array[13]
                append_array.append(price_column)
                append_array.append(len(item_array))
                print(f"会社番号→{company_dict[item_array[8]]}")
                
                # 初めての辞書追加
                new_array =[]
                new_array.append(append_array)
                insert_data[item_array[1]]=new_array
                
                return_All_array.append(append_array)
                # print(append_array,"これは初めての値")
            
           
            for key, value in insert_data.items():
                print(f"キー: {key}, 値: {value}")
            grouped_data[ref_number].append(item)
            # エクセルデータをいったん保存する
            
       #結果の出力
       #会社IDが同じ場合、二次元配列にする。
    #    header = ('JWA-開催日-箱番号-番号', '品番', '', '', '', '', '', '', '', '落札価格', 'noching')
       # 各リファレンス番号ごとにデータをまとめて出力
    #    for ref_number, items in grouped_data.items():
    #        if len(items) > 0:
    #           combined_data = [ref_number]
    #           before_dict = {}
    #           after_dict = {}
    #           valuenum = 0
    #           insert_value = []
    #           for item in items:
    #               after_insert_value = []
    #               if not item[8] in before_dict:
    #                  before_dict[item[8]] = valuenum 
    #                  new_itemlist = list(item)       
    #                  indices_to_remove = [0, 8]
    #                  for index in sorted(indices_to_remove,reverse=True):
    #                     del new_itemlist[index]
    #                  insert_value.append(new_itemlist)
    #                  valuenum += 1
    #               else:
    #                  column = before_dict[item[8]]
    #                   # after_insert_value=[]に入れ込む
    #                   # 列番号:[k]という構図　値段を[k]番目に修正する。
    #                  after_dict[column] = item[9]
    #           combined_data.extend(item[2:]) # リファレンス番号以外のデータを追加
    #        for value in insert_value:
    #             return_All_array.append(value)
    #        for key ,value in after_dict.items():
    #             #  valueのながさの配列を作り、value番目にvalueの値を入れ込む
    #              append_array = [""] * 8
    #              append_array[7+key] = value
    #             #  値段のみが入る
    #              return_All_array.append(append_array)

    #    先頭行に会社名を追加している
       for key in company_dict:
        print(key)
        header.append(key)
       return_All_array.insert(0,header)
       return return_All_array
        

    def insert_data(self,values):
            # 動的なプレースホルダーのリスト
            
            placeholders = ', '.join(['?'] * (len(self.fields)))
            print(self.table_name)
            print(placeholders)
            # 一番目にfieldcountを入れ込む
            # incrementnum = self.fieldcountAllcountcheck()
            # values.insert(0,incrementnum)
            print(self.fields,"←値確認この数も合わせなければならない")
            print(values)
            print("ここでエラーになる")
            # 動的なフィールドのリストを文字列に変換
            fields_str = ', '.join(self.fields)
            # ここでクエリを検索して存在確認し、それのidを取得してincrementnumを上書きする。
            # 動的なクエリを生成

            query = f"INSERT OR REPLACE INTO {self.table_name} ({fields_str}) VALUES ({placeholders})"
            print(query)
            self.cursor.execute(query, values)
            # 
            
            self.conn.commit()  # トランザクションをコミット

    
    def insert_watch_item(self, table_name,bucherer_watch_id, year, model_name, ref, bracelet, dial, url):
        try:
            # self.cursor.execute('''INSERT INTO {}(bucherer_watch_id, year, model_name, ref, bracelet, dial, url) VALUES (?, ?, ?, ?, ?, ?, ?)'''.format(table_name),
            #(bucherer_watch_id, year, model_name, ref, bracelet, dial, url))
            query = '''INSERT OR REPLACE INTO {} (bucherer_watch_id, year, model_name, ref, bracelet, dial, url) VALUES (?, ?, ?, ?, ?, ?, ?)'''.format(table_name)
            self.cursor.execute(query, (bucherer_watch_id, year, model_name, ref, bracelet, dial, url))
            self.conn.commit()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print("Error occurred while inserting data:", e)
    
    # 渡された日付 + 4日分を検索する。日付は呼び出し元で設定する配列を返すメソッドにする予定。
    def weeksitemdiffcheck(self,days):
        #  日付n日分を全て検索そのアイテムをn+1,n+2....に存在するか確認存在した場合、配列のn+k番目に代入する。→独自のテーブルを作る？n+kで独自のテーブルを検索して存在した場合、true
         for day in days:
              print(day)
            #   日付nのアイテムループする。
         return

    def close_connection(self):
        self.conn.close()
