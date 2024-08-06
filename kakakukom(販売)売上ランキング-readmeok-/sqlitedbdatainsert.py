import sqlite3
import datetime
def connect_db():
    
    # return sqlite3.connect('kakakukomocopy.db')
    return sqlite3.connect('kakakukomo.db')


# date
def insert_watch_item(kakakukom_watch_id, model_name, ref, nowprice, usenowprice, bracelet, dial, url):
    conn = connect_db()
    c = conn.cursor()
    try:
        print(f"価格コムのID：{type(kakakukom_watch_id)} モデル名:{type(model_name)} リファレンス:{type(ref)} ブレスレット:{type(bracelet)} ダイアル:{type(dial)} URL:{type(url)}")
        c.execute('''
        INSERT OR REPLACE INTO watch_item (kakakukom_watch_id, model_name, ref, bracelet, nowprice, usenowprice, dial, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (kakakukom_watch_id, model_name, ref, bracelet, nowprice, usenowprice, dial, url))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"データ挿入に失敗しました。制約違反が発生しました: {e}")
        print(kakakukom_watch_id)
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
    finally:
        conn.close()

def insert_weekly_report(week_start_date, ranking, summary, price, kakakukom_watch_id):
    conn = connect_db()
    c = conn.cursor()
    # クエリを実行して存在している場合、continue
    # c.execute("SELECT COUNT(*) FROM weekly_reports WHERE week_start_date = '2024/05/09' AND kakakukom_watch_id = kakakukom_watch_id")
    # 以下変数利用する場合

    c.execute("SELECT COUNT(*) FROM weekly_reports WHERE week_start_date = ? AND kakakukom_watch_id = ?", (week_start_date, kakakukom_watch_id))
    result = c.fetchone()  # クエリの結果を取得
    # クエリ実行して存在しない場合、returnする
    if result[0] >= 1:
        return
   
    c.execute('''
    INSERT INTO weekly_reports (week_start_date, ranking, summary, price, kakakukom_watch_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (week_start_date, ranking, summary, price, kakakukom_watch_id))
    conn.commit()
    conn.close()

# 数を返す
def count_watch_items():
    try:
        # データベース接続を確立
        conn = connect_db()
        c = conn.cursor()

        # watch_item テーブルのレコード数をカウント
        c.execute("SELECT COUNT(*) FROM watch_item")
        result = c.fetchone()  # クエリ結果の取得

        # 結果を表示または他の処理
        print("Total number of watch items:", result[0])

    except Exception as e:
        # エラーが発生した場合の処理
        print(f"An error occurred: {e}")

    finally:
        # データベース接続を閉じる
        conn.close()

    return result[0]  # カウントされたレコード数を返す

def datagetcount(date):
    # 日付を指定
    conn = connect_db()
    c = conn.cursor()
    items = []
    #  SELECT COUNT(*) FROM weekly_reports  WHERE summary = "2024/05/14";  
    #  SELECT * FROM weekly_reports  WHERE summary = "2024/05/14";  
    # c.execute("SELECT COUNT(*) FROM weekly_reports WHERE summary = ?", (date,))
    # 本日もしくは近似日検索する。値は一:多で返ってくる。
    # c.execute("SELECT * FROM weekly_reports WHERE summary = ?", (date,))
   

    # c.execute("SELECT * FROM weekly_reports WHERE kakakukom_watch_id IN (SELECT MIN(kakakukom_watch_id) FROM weekly_reports GROUP BY summary) AND summary = ?", (date,))
    # SELECT DISTINCT kakakukom_watch_id FROM weekly_reports WHERE summary = '2024/05/14';
    # idの重複を削除し、かつ日付で検索する。
    # c.execute("""SELECT DISTINCT kakakukom_watch_id FROM weekly_reports WHERE summary = ?""", (date,))
    # c.execute("""SELECT DISTINCT kakakukom_watch_id FROM weekly_reports WHERE summary = ? """, (date,))
    
    # top10の順番で抽出する。
    for i in range (1,11):
        # ランキングかつ、日付でとる。
        rankingstr = str(i)
        c.execute("""SELECT DISTINCT kakakukom_watch_id FROM weekly_reports WHERE summary = ? AND ranking = ? """, (date, rankingstr,))
        # c.execute("""SELECT price FROM weekly_reports WHERE kakakukom_watch_id = ? AND week_start_date = ?""", (kakakukom_watch_id, latest_date.strftime('%Y/%m/%d'),))
        print(i)
        # print(c.fetchall())
        result = c.fetchall()
        print(f"{result}は欲しい値")

        if result:
            # タプル型を全て文字列に変換する
            for item in result:
                item_string = item[0] # タプル内の要素を文字列に変換
                items.append(item_string)
        else:
            print("空です")
            continue
        if len(items) >= 10:
            return items
 
    
    # print(result)
    # クエリ数を返す。
    print(items)
    return items


def watch_item_only_get(kakakukom_watch_id):
    # 検索
    conn = connect_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM watch_item WHERE kakakukom_watch_id = ? """,(kakakukom_watch_id,))
    result = c.fetchall()
    return result

def weekly_reports_only_get(kakakukom_watch_id,date):
    # 検索
    conn = connect_db()
    c = conn.cursor()
   
    # クエリの実行
    # c.execute("""SELECT * FROM weekly_reports WHERE kakakukom_watch_id = ? AND summary = ?""", (kakakukom_watch_id, date))
    c.execute("""SELECT * FROM weekly_reports WHERE kakakukom_watch_id = ? """, (kakakukom_watch_id,))
    result = c.fetchall()
    # 日付取得のためのクエリ
    c.execute("""SELECT week_start_date FROM weekly_reports WHERE kakakukom_watch_id = ?""", (kakakukom_watch_id,))
    date = c.fetchall()
    dates = [datetime.datetime.strptime(date[0], '%Y/%m/%d') for date in date if date[0]]
    # 日付を新しい順にソート
    dates.sort(reverse=True)
    
    # 最新の日付とその直前の日付を取得
    if dates:
        dateitems = []
        latest_date = dates[0]
        # 最新の日付から7日前の日付を計算
        seven_days_before = latest_date - datetime.timedelta(days=7)
        # 7日前の日付がリストに存在するかチェック
        exists = seven_days_before in dates
        nearest_date = dates[1] if len(dates) > 1 else None
        # 全ての日付データを抽出する。
        # 日付の数だけ、ループする。
        for date in dates:
            print(date)
            print(date.strftime('%Y/%m/%d'))
            # アイテムごとの日付の値段
            c.execute("""SELECT price FROM weekly_reports WHERE kakakukom_watch_id = ? AND week_start_date = ? """, (kakakukom_watch_id, date.strftime('%Y/%m/%d')))
            price = c.fetchall()
            # 金額のタプル型をなおして数字をとりだす。
            price = [t[0]for t in price]
            price = price[0]
            
            format_data = {date.strftime('%Y/%m/%d'):{"price":price}}
            dateitems.append(format_data)

            print(f"シリアルナンバー:{kakakukom_watch_id}日付:{date.strftime('%Y/%m/%d')}値段:{price}")
        print(f"{dateitems}は週ごとの配列データ")
        return dateitems
        if not exists:
            # 一週間前が存在しない場合、直近の日付を入れる。
            seven_days_before = nearest_date
            print(f"{latest_date}{seven_days_before}ここは七日前が存在しない場合表示される")
            
        if nearest_date == None:
             c.execute("""SELECT price FROM weekly_reports WHERE kakakukom_watch_id = ? AND week_start_date = ?""", (kakakukom_watch_id, latest_date.strftime('%Y/%m/%d'),))
        else:
             # 存在する場合、クエリを投げて、最新の日付の値段を取得する。
             c.execute("""SELECT price FROM weekly_reports WHERE kakakukom_watch_id = ? AND week_start_date = ? """, (kakakukom_watch_id, latest_date.strftime('%Y/%m/%d')))
             c.execute("""SELECT price FROM weekly_reports WHERE kakakukom_watch_id = ? AND week_start_date = ? AND week_start_date=?""", (kakakukom_watch_id, latest_date.strftime('%Y/%m/%d'),seven_days_before.strftime('%Y/%m/%d')))
             c.execute("""SELECT price FROM weekly_reports WHERE kakakukom_watch_id = ? AND week_start_date IN (?, ?)""", (kakakukom_watch_id, latest_date.strftime('%Y/%m/%d'),seven_days_before.strftime('%Y/%m/%d')))

        
       
        
        # 日付ごとの値段が代入される。
        price = c.fetchall()
        # 逆にする。
        price = price[::-1]
        price = [item[0] for item in price]
        print(price)
        # 辞書型を呼び出し元へ返す。
        # [latest_date:{price:金額,date:日付},seven_days_before:{price:金額,date:日付}]
        # result_dict = [{'latest_date': latest_date.strftime('%Y/%m/%d'), 'seven_days_before': seven_days_before.strftime('%Y/%m/%d'), 'price': row[0]} for row in price]
        # print(result_dict)
        #値段と日付を返す、 辞書を作成。
        if len(price) >= 2:
            formatted_data = {
            'latest_date': {'price': price[0], 'date': latest_date.strftime('%Y/%m/%d')},
            'seven_days_before': {'price': price[1], 'date': seven_days_before.strftime('%Y/%m/%d')}}
        elif len(price) <= 1:
            formatted_data = {
            'latest_date': {'price': price[0], 'date': latest_date.strftime('%Y/%m/%d')},
            'seven_days_before': {'price':"", 'date': ""}
            }
        else:
            formatted_data = {
             'latest_date':{'price':"", 'date': ""},
             'seven_days_before': {'price':"", 'date': ""}
            } 
        print(formatted_data)
        return formatted_data
        print(f"最新の日付: {latest_date.strftime('%Y/%m/%d')}")
        # print(f"その直前の日付: {nearest_date.strftime('%Y/%m/%d')}" if nearest_date else "直前の日付は存在しません")
        print(f"七日前の日付: {seven_days_before.strftime('%Y/%m/%d')}")
    # デイリーデータが存在しない場合
    else:
        formatted_data = {
             'latest_date':{'price':"", 'date': ""},
             'seven_days_before': {'price':"", 'date': ""}
            }
        return formatted_data
    
   
# def dateallget(date)