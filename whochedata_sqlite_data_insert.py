from sqlite_data_insert import SQLiteDataInsert
import sqlite3
import os
import time
from datetime import datetime
class WhocheSqliteDataInsert(SQLiteDataInsert):
    def __init__(self,db_file):
        # db名をわたす、そして、そのdbを探索し、テーブル、フィールドを渡す。最終的にはアクセス可能なテーブル一覧を返す?
            # テーブル一覧を取得するSQLクエリs
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        # テーブルの詳細を辞書型にする。テーブル名をキーに、値をフィールド名にする、、、
        self.tablesdateill= {}
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        # SQLクエリを実行してテーブル名を取得
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        today_date_and_time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.db_logfile_name = f"dbログ_{today_date_and_time}.txt"
        # 取得したテーブル名をリストに格納
        self.table_names = [table[0] for table in tables]
        # フィールド名を取得する。
        for table in self.table_names:
            print("ここでフィールド名を取得し、辞書型で返す。")
            self.cursor.execute(f"PRAGMA table_info({table})")
            # ここで強制的に排除する？
            columns = self.cursor.fetchall()
            # print(columns)
            # フィールドをループする。
            columun = []
            for fieldname in columns:
                # 以下はフィールド名
                # print(fieldname)
                print(fieldname[1])

                columun.append(fieldname[1])
                # プロパティに持たせるインスタンスを作成して、それを辞書型にする。その辞書型の中には、
                # dbに応じた処理を持つ変数が格納されている。
            # クラスメソッドを作成する。
            instanse = SQLiteDataInsert(db_file,table,columun)
            self.tablesdateill[table] = instanse
            # print(self.tablesdateill)
            # super().__init__(db_file,table,columns)
            # フィールド名は2番目に格納されている。
    
    def save_logs_to_file(logs, file_path):
    # ここでアイテム一覧の配列を作ってしまう。
    # ここでの配列は二つで一つの二次元配列になる。
     with open(file_path, "a", encoding="utf-8") as file:
        file.write(str(logs) + "\n")
    

    def groupby(self,groupcolomn="test"):
        #  query = "SELECT name FROM sqlite_master WHERE type='table'"
        # SELECT 表示させるカラム名 FROM テーブル名 GROUP BY グループ化するカラム名;
        #  query = f"""SELECT COUNT(*) FROM {self.table_name} WHERE {all_field_query}"""
        query = f"SELECT * FROM watch_item GROUP BY ref"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results


    
    def close_connection(self):
         if self.conn:
            self.conn.close()
            self.conn = None
    def save_logs_to_file(self,logs, file_path):
        with open(file_path, "a", encoding="utf-8") as file:
             file.write(str(logs) + "\n")
    def instansemake(self,value):
        #  色々使える。インスタンスを返す。呼び出し元でメソッドを利用する。
         print("親クラスを利用するためのインスタンス作成する。")

        #  self.d
         instance = ""
         return instance

    def insertsuper(self,value):
            # ここでインスタンス側から渡されたデータを処理する。
            print(value,"は入れる値")

            super().insert_data(value)  

    def all_datacheck(self,value,day):
        # watch_item のなかの一致するアイテムを全て取得する。
        print("データ抽出")
        # self.cursor.execute(f"""SELECT * FROM {teb}""")       
    # 値検索ですべてのアイテムを返す
    def days_diffcheck(self,settingtablename,value,daysArray):
        print(value,"←メソッドに渡された値")
        # 日付が二つわたされる。
        # 日付1n で全検索、日付1の全値が返ってくるので、それをループ
        # 日付1値×他日付ループ
        # ヒットした場合連想配列n番目に追加
        # 他日付ループでヒットしない場合、continue
        # 日付ループ終了
        # 日付1　n-1ループへ
        # 処理がすべて終了した場合、配列を返す
        # days.remove(value)
        # 日付ループする。
        temptablesString = ""
        for day in daysArray:
            #  日ごとテーブルを作成する。
            temptebalename = "temp_"+ day.replace("/","_")
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (temptebalename,))
            tempfilecheck = self.cursor.fetchone()
            if tempfilecheck:
                 print(temptebalename)
                 self.cursor.execute(f"DROP TABLE IF EXISTS {temptebalename}")
            # 一時ファイルの削除、一時ファイルが存在する場合、削除、しない場合、作成。
            print(temptebalename,"は一時テーブル確認")
            self.cursor.execute(f"DROP TABLE IF EXISTS {temptebalename}")
            self.cursor.execute(f"""CREATE TEMP TABLE {temptebalename} AS SELECT * FROM {settingtablename} WHERE weekdate = ?""", (day,))
            self.cursor.execute(f"""SELECT * FROM {temptebalename}""")
            temptablesString += temptebalename + ","
            item = self.cursor.fetchall()
            print(temptablesString)
        temp_tables_list = temptablesString.split(",")
        print(temp_tables_list)
       
        intersect_query = " INTERSECT ".join([f"SELECT bucherer_watch_id FROM {table}" for table in temp_tables_list[:-1]])   
        # 和集合を取得
        all_union_query = " UNION ".join([f"SELECT bucherer_watch_id, weekdate FROM {table}" for table in temp_tables_list[:-1]])   
        print(f"{intersect_query}は積集合クエリ")
        union_query = f"""
        CREATE TEMP TABLE ALLUNIONTABLE AS
        SELECT *
        FROM {temp_tables_list[0]}
        WHERE bucherer_watch_id IN ({intersect_query})
        """

        self.cursor.execute("DROP TABLE IF EXISTS WatchID_Intersect")
        print(all_union_query,"をチェック")
        self.cursor.execute(f"""CREATE TEMP TABLE WatchID_Intersect AS SELECT bucherer_watch_id, weekdate FROM ( {all_union_query} ) AS all_dates;
         """)
        self.cursor.execute("SELECT * FROM WatchID_Intersect")
        # print(self.cursor.fetchall(),"ここ")
        data = self.cursor.fetchall()
        # 
        # IDごとに一致する日付をリストとして格納する辞書を作成する
        id_dates_dict = {}
        for id, date in data:
             if id not in id_dates_dict:
                  id_dates_dict[id] = []
             id_dates_dict[id].append(date)
             


        # 結果の表示
        for id, dates in id_dates_dict.items():
             print(f"ID: {id}, Dates: {dates}")

        # self.conn.close()
        return id_dates_dict
        

      
             
       
    
        print(f"{union_query}はすべてクエリ")
        # union_query = "CREATE TEMP TABLE ALLUNIONTABLE AS " + " INTERSECT ".join([f"SELECT bucherer_watch_id {table}" for table in temp_tables_list])
        # union_query = "CREATE TEMP TABLE ALLUNIONTABLE AS SELECT * FROM temp_2024_05_23 UNION SELECT * FROM temp_2024_05_22 UNION SELECT * FROM temp_2024_05_21 UNION SELECT * FROM temp_2024_05_20"
        # union_query = "CREATE TEMP TABLE ALLUNIONTABLE AS SELECT bucherer_watch_id FROM temp_2024_05_20 UNION SELECT bucherer_watch_id FROM temp_2024_05_21"
        # union_query = "SELECT bucherer_watch_id FROM temp_2024_05_20 INTERSECT SELECT bucherer_watch_id FROM temp_2024_05_21"
        
        self.cursor.execute(union_query)
        intersectdata = self.cursor.fetchall()
        print(intersectdata,"検索けっか　")
        # 積集合,4つあつまるテーブルをつくる




        query = f'SELECT * FROM {settingtablename} WHERE {value}'
        
        self.cursor.execute(query)
        items = self.cursor.fetchall()
        # print(items)
        
        temptebalename = "temp_"+value.replace("/","_")
        print(f"{value}は日付{settingtablename}はテーブル名 {temptebalename}は一時テーブル名")
        # self.cursor.execute(f"""CREATE TEMP TABLE {value} AS SELECT * FROM {settingtablename} WHERE weekdate = ?""", (value,))
        self.cursor.execute(f"""CREATE TEMP TABLE {temptebalename} AS SELECT * FROM {settingtablename} WHERE weekdate = ?""", (value,))
        self.cursor.execute(f"""SELECT * FROM {temptebalename}""")
        item = self.cursor.fetchall()
        for i in item:
             print(i)
             print("----")
        
        self.cursor.execute(f"DROP TABLE IF EXISTS {temptebalename}")
        for index,day in enumerate(daysArray):
            # self.cursor.execute(f"""CREATE TEMP TABLE {day} AS SELECT * FROM {settingtablename} WHERE date = ?""", (value,))

            #  渡した日付と配列が一致していた場合処理抜ける。通常は配列からとりのぞけばいいが、もとの配列に影響するため却下
            if day in value:
                  print(f"{day}と{value}")
                  continue
            
            # アイテムをループする。
        # 各アイテムは、カウントでチェック！！
        # print(items)
        # for item in items:
        #      print(item)
        #      print("--------")
        
    

        # self.cursor.execute(f"SELECT MAX({self.fields[0]}) FROM {self.table_name}")

       
        # valueですべての値を検索する。



        # super().__init__(db_file,wath_item_table,wath_item_fields)
        # 初期でdbを検索して、オブジェクト型にして、そのなかにフィールドを持たせる
    # 時計データを入力する
    def watch_item_insert(self,value):
        # 時計一覧のテーブル名
        wath_item_table = 'watch_item'
        wath_item_fields = ['bucherer_watch_id','year','model_name','ref','bracelet','dial','url']
        watch_item_insert_instance = SQLiteDataInsert(self.dbname,wath_item_table,wath_item_fields)
    # weekly_reports一覧