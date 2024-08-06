import sqlite3

class DatabaseManager:
    def __init__(self, db_filename):
        """データベースに接続し、カーソルを初期化します。"""
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()

    def insert_watch_item(self, watch_items):
        """watch_item テーブルにデータを挿入します。
        
        Args:
            watch_items (list of tuple): (kakakukom_watch_id, model_name, ref, url) 形式のタプルリスト
        """
        insert_query = 'INSERT INTO watch_item (kakakukom_watch_id, model_name, ref, url) VALUES (?, ?, ?, ?)'
        self.cursor.executemany(insert_query, watch_items)
        self.conn.commit()

    def insert_weekly_reports(self, reports):
        """weekly_reports テーブルにデータを挿入します。
        
        Args:
            reports (list of tuple): (week_start_date, ranking, summary, price, kakakukom_watch_id) 形式のタプルリスト
        """
        insert_query = 'INSERT INTO weekly_reports (week_start_date, ranking, summary, price, kakakukom_watch_id) VALUES (?, ?, ?, ?, ?)'
        self.cursor.executemany(insert_query, reports)
        self.conn.commit()

    def close(self):
        """データベース接続を閉じます。"""
        self.conn.close()
