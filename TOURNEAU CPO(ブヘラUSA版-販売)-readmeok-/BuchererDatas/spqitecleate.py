import sqlite3

conn = sqlite3.connect('TOURNEAU.db')

# カーソルオブジェクトの作成
c = conn.cursor()


# カーソルオブジェクトの作成
c = conn.cursor()

# テーブルの作成
# ブヘラのアイテムDB
c.execute('''
CREATE TABLE IF NOT EXISTS watch_item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bucherer_watch_id TEXT NOT NULL UNIQUE,
    year TEXT,
    model_name TEXT NOT NULL,
    ref TEXT,
    size TEXT,
    bracelet TEXT,
    dial TEXT,
    url TEXT NOT NULL
)
''')

# 値段DB
# weekly_reports テーブルを作成
# watch_item weekly_reports 1:n
c.execute('''
CREATE TABLE IF NOT EXISTS weekly_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    weekdate TEXT NOT NULL,
    ranking TEXT,
    price INTEGER,
    bucherer_watch_id TEXT NOT NULL,  
    FOREIGN KEY (bucherer_watch_id) REFERENCES watch_item(bucherer_watch_id)
)
''')

# コミット（変更をデータベースに反映させる）
conn.commit()

# コネクションを閉じる
conn.close()
