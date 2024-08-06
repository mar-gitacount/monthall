import sqlite3

# データベースに接続
conn = sqlite3.connect('kakakukomo.db')

# カーソルオブジェクトの作成
c = conn.cursor()

# テーブルの作成
# 価格コムのアイテムDB
c.execute('''
CREATE TABLE IF NOT EXISTS watch_item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    kakakukom_watch_id TEXT NOT NULL UNIQUE,
    model_name TEXT NOT NULL,
    ref TEXT,
    bracelet TEXT,
    dial TEXT,
    url TEXT NOT NULL,
    nowprice INTEGER,
    usenowprice INTEGER
          
)
''')

# 値段DB
# weekly_reports テーブルを作成
c.execute('''
CREATE TABLE IF NOT EXISTS weekly_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_start_date TEXT NOT NULL,
    ranking TEXT,
    summary TEXT,
    price INTEGER,
    kakakukom_watch_id TEXT NOT NULL,  
    FOREIGN KEY (kakakukom_watch_id) REFERENCES watch_item(kakakukom_watch_id)
)
''')

# コミット（変更をデータベースに反映させる）
conn.commit()

# コネクションを閉じる
conn.close()
