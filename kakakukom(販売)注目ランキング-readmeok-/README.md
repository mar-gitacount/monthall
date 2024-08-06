# README

## 概要

このプロジェクトは、価格コム(注目ランキング)からデータを抽出し、そのデータをSQLite3データベースに保存する `scriping.py` と、そのデータをExcelファイルに保存する `datagetexcelinsert.py` から構成されています。

## ファイル構成

- `scriping.py`: 価格コム(注目ランキング)からデータをスクレイピングし、SQLite3データベースに保存します。
- `datagetexcelinsert.py`: SQLite3データベースからデータを取得し、Excelファイルに保存します。

## 必要なライブラリ

以下のPythonライブラリが必要です。これらは `requirements.txt` ファイルに記載されています。

- requests
- BeautifulSoup4
- sqlite3
- pandas
- openpyxl

インストール方法:
```sh
pip install -r requirements.txt

実行ファイル1:
```sh 
python scriping.py

実行ファイル2:
```sh
python datagetexcelinsert.py