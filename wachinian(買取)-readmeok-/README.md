# README

## 概要

このプロジェクトは、ウォッチニアンのサイト(売上)からデータを抽出し、そのデータをエクセルに保存する `webdriver2.py`から構成されています。

## ファイル構成

- `webdriver2.py`:ウォッチニアンのサイト(売上)データをスクレイピングし、SQLite3データベースに保存します。

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

実行コマンド1:
```sh
python webdriver2.py

