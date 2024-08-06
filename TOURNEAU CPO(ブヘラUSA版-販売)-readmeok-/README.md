# README

## 概要

このプロジェクトは、TOURNEAU CPOから`usaBuchererdataget.py `を使ってデータを抽出し、そのデータを `BuchererMainDatas.json` に保存したあと  `jsondataloadmakeexcel.py`  でエクセルファイルに吐き出す。
## ファイル構成

- `usaBuchererdataget.py`: TOURNEAU CPOからデータをスクレイピングし、`BuchererMainDatas.json`に保存します。
- `jsondataloadmakeexcel.py`: `BuchererMainDatas.json`からデータを取得し、Excelファイルに保存します。

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
python usaBuchererdataget.py

実行コマンド:
```sh
python jsoninsert.py

実行コマンド3:
```sh
python jsondataloadmakeexcel.py