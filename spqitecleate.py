import sqlite3

conn = sqlite3.connect('bucherer.db')
c = conn.cursor()

# ブヘラのアイテムDB
c.execute('''
CREATE TABLE IF NOT EXISTS watch_item (
    item_id TEXT PRIMARY KEY,
    ref TEXT NOT NULL,
    year TEXT,
    model_name TEXT NOT NULL,
    size TEXT,
    bracelet TEXT,
    dial TEXT,
    url TEXT NOT NULL,
    company_name TEXT,
    price INTEGER,
    extraction_date TEXT,
    ather_data TEXT
)
''')

# 値段DB
c.execute('''
CREATE TABLE IF NOT EXISTS weekly_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    weekdate TEXT NOT NULL,
    ranking TEXT,
    price INTEGER,
    ref TEXT NOT NULL, 
    company_name TEXT,
    item_id INTEGER,
    FOREIGN KEY (item_id) REFERENCES watch_item(item_id)
)
''')

# 既存のテーブルに新しいカラムを追加
conn.execute('ALTER TABLE watch_item ADD COLUMN other_data TEXT')
# コミット（変更をデータベースに反映させる）
conn.commit()

# コネクションを閉じる
conn.close()
