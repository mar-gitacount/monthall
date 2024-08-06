# README

## 概要

このプロジェクトは、JBA(オークションサイト)からデータを抽出し、そのデータをエクセルファイルに保存する `csv.py` を実行し、"csvフォルダ内"に存在するJBAのcsvファイルを読み込み再生成する。
なお、実行が終わったら、そのcsvファイルは済みフォルダに移動する！！

## ファイル構成

- `csv.get`:csv/○○.csvファイルを読み込んで、新しいcsvファイルを作成する。
- `csv(dir)`:オークションサイトからダウンロードしてきたcsvファイルを格納するフォルダ。python実行後そのcsvファイルは済みフォルダに移動する。
- `出品一覧_yyyy/mm/dd/tttt.csv`: オークションサイトからダウンロードしてきたcsvファイル、 `csv.get` 実行完了後、`csv/済み`　に移動する。

## 必要なライブラリ

以下のPythonライブラリが必要です。これらは `requirements.txt` ファイルに記載されています。

- requests==2.26.0
- beautifulsoup4==4.10.0
- pandas==1.3.4
- openpyxl==3.0.9

インストール方法:
```sh
pip install -r requirements.txt

実行ファイル

```sh
python csv.py
