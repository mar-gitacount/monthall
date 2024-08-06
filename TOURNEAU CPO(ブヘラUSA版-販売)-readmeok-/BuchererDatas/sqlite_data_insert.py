# sqlite_data_insert.py

import sqlite3

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
