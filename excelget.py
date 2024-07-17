from openpyxl import Workbook, load_workbook
import os
import re
from datetime import datetime
import shutil
from whochedata_sqlite_data_insert import WhocheSqliteDataInsert


def copy_folder(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    try:
        shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)
        print(f"Folder copied from {src_folder} to {dest_folder}")
    except Exception as e:
        print(f"Error: {e}")

# ウォッチニアンのデータをデータベースに入稿する処理
def watchnian(instance):
    current_directory = os.getcwd()
    folder_name = "まとめるエクセル"
    new_directory = os.path.join(current_directory, folder_name)
    items = instance.tablesdateill
    watch_item_instance = items["watch_item"]
    pattern = re.compile(r'^ウォッチニアン.*\.xlsx$')


def gmt(instance):
    current_directory = os.getcwd()
    folder_name = "まとめるエクセル"
    new_directory = os.path.join(current_directory, folder_name)
    items = instance.tablesdateill
    watch_item_instance = items["watch_item"]
    # 年と月を抽出する正規表現パターン
    yearmonthpattern = re.compile(r'(\d{4})-(\d{2})')
    # フィールドを再定義する。
    # watch_item_instance.fields = ["item_id","ref","year","size","bracelet","dial","url"]
    # insert_values = [insert_date,"0",price,bucherer_watch_id]
    # print(insert_values)
    # watch_item_instance.insert_data(insert_values)
    # JWAファイル取得
    pattern = re.compile(r'^GMT.*\.xlsx$')
    jwa_files = []

    # ディレクトリ内のファイルを走査して、JWAファイルをリストに追加する
    for file in os.listdir(new_directory):
        if pattern.match(file):
            jwa_files.append(os.path.join(new_directory, file))
    for file in jwa_files:
        full_path = os.path.join(new_directory, file)
        workbook = load_workbook(full_path, data_only=False)
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            for row in sheet.iter_rows(values_only=True):
                print(list(row))
                rowitemslist = list(row)
                # 週フィールド名
                # weekly_table_fields = ['weekdate','ranking','price','bucherer_watch_id']
                # # 週レポート
                # weekly_report_inset_instance = SQLiteDataInsert(dbname,weekly_table_name,weekly_table_fields)
                # insert_values = [rowitemslist[1],"",rowitemslist[16],rowitemslist[10],"","",""]
                # insert_values = [rowitemslist[10],"",rowitemslist[16],"","","",""]
                # EVENCEのidはURLの一番下から抽出する。
                ref = rowitemslist[1]
                year = ""
                model_name = rowitemslist[0]
                size =""
                dial = ""
                bracelet = rowitemslist[2]
                # 値段判定
                if rowitemslist[3]:
                    price = rowitemslist[3]
                else:
                    price = rowitemslist[4]
                url = rowitemslist[5]
                print(url)
                match = re.search(r'/products/detail/(\d+)', url)
                if match:
                    product_id = match.group(1)
                    print(product_id)
                else:
                    print("Product ID not found")
                    continue
                make_ID = "Evence-"+product_id
                print(make_ID)




                yearmonthmatch = yearmonthpattern.match(str(file))
                yearmonthmatch = re.search(r'(\d{4}-\d{2})', file)
                if yearmonthmatch:
                    formatted_date = yearmonthmatch.group(1)  # 年月を取得する
                    formatted_date = datetime.strptime(formatted_date, '%Y-%m')
                    formatted_date_str = formatted_date.strftime('%Y/%m')
                    
                    # print(year)
                    # month = yearmonthmatch.group(2)  # 月の部分を取得
                    # formatted_date = f"{year}/{month}"
                    print(f"Formatted date: {formatted_date_str}")
                else:
                    
                    print(f"Date format doesn't match expected pattern.{file}")
                    formatted_date = "noching"
                
                # 品番?
                # if rowitemslist[10] is None:
                #     # rowitemslist[10] が None の場合の処理
                #     print("rowitemslist[10] は None です")
                #     ref = "なし"
                # else:
                #      # rowitemslist[10] が None でない場合の処理
                #      print("rowitemslist[10] は None ではありません")
                #      ref = rowitemslist[10] 
                    
                # ↓あとで使うやつ
                # ↓その他アイテム
                
                watch_item_instance.insert_data([make_ID,ref,year,model_name,size,bracelet,dial,url,"EVENCE",price,formatted_date_str,"その他"])

                # watch_item_instance.fieldcountAllcountcheck()
                row_data = []
                # dbにデータを入れる
                # for cell in row: 
                #     print(str(cell))      
            # insert_values = [insert_date,"0",price,bucherer_watch_id]
    return jwa_files






def evence(instance):
    current_directory = os.getcwd()
    folder_name = "まとめるエクセル"
    new_directory = os.path.join(current_directory, folder_name)
    items = instance.tablesdateill
    watch_item_instance = items["watch_item"]
    # 年と月を抽出する正規表現パターン
    yearmonthpattern = re.compile(r'(\d{4})-(\d{2})')
    # フィールドを再定義する。
    # watch_item_instance.fields = ["item_id","ref","year","size","bracelet","dial","url"]
    # insert_values = [insert_date,"0",price,bucherer_watch_id]
    # print(insert_values)
    # watch_item_instance.insert_data(insert_values)
    # JWAファイル取得
    pattern = re.compile(r'^EVANCE.*\.xlsx$')
    jwa_files = []

    # ディレクトリ内のファイルを走査して、JWAファイルをリストに追加する
    for file in os.listdir(new_directory):
        if pattern.match(file):
            jwa_files.append(os.path.join(new_directory, file))
    for file in jwa_files:
        full_path = os.path.join(new_directory, file)
        workbook = load_workbook(full_path, data_only=False)
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            for row in sheet.iter_rows(values_only=True):
                print(list(row))
                rowitemslist = list(row)
                # 週フィールド名
                # weekly_table_fields = ['weekdate','ranking','price','bucherer_watch_id']
                # # 週レポート
                # weekly_report_inset_instance = SQLiteDataInsert(dbname,weekly_table_name,weekly_table_fields)
                # insert_values = [rowitemslist[1],"",rowitemslist[16],rowitemslist[10],"","",""]
                # insert_values = [rowitemslist[10],"",rowitemslist[16],"","","",""]
                # EVENCEのidはURLの一番下から抽出する。
                ref = rowitemslist[1]
                year = ""
                model_name = rowitemslist[0]
                size =""
                dial = ""
                bracelet = rowitemslist[2]
                # 値段判定
                if rowitemslist[3]:
                    price = rowitemslist[3]
                else:
                    price = rowitemslist[4]
                url = rowitemslist[5]
                print(url)
                match = re.search(r'/products/detail/(\d+)', url)
                if match:
                    product_id = match.group(1)
                    print(product_id)
                else:
                    print("Product ID not found")
                    continue
                make_ID = "Evence-"+product_id
                print(make_ID)




                yearmonthmatch = yearmonthpattern.match(str(file))
                yearmonthmatch = re.search(r'(\d{4}-\d{2})', file)
                if yearmonthmatch:
                    formatted_date = yearmonthmatch.group(1)  # 年月を取得する
                    formatted_date = datetime.strptime(formatted_date, '%Y-%m')
                    formatted_date_str = formatted_date.strftime('%Y/%m')
                    
                    # print(year)
                    # month = yearmonthmatch.group(2)  # 月の部分を取得
                    # formatted_date = f"{year}/{month}"
                    print(f"Formatted date: {formatted_date_str}")
                else:
                    
                    print(f"Date format doesn't match expected pattern.{file}")
                    formatted_date = "noching"
                
                # 品番?
                # if rowitemslist[10] is None:
                #     # rowitemslist[10] が None の場合の処理
                #     print("rowitemslist[10] は None です")
                #     ref = "なし"
                # else:
                #      # rowitemslist[10] が None でない場合の処理
                #      print("rowitemslist[10] は None ではありません")
                #      ref = rowitemslist[10] 
                    
                # ↓あとで使うやつ
                # ↓その他アイテム
                
                watch_item_instance.insert_data([make_ID,ref,year,model_name,size,bracelet,dial,url,"EVENCE",price,formatted_date_str,"その他"])

                # watch_item_instance.fieldcountAllcountcheck()
                row_data = []
                # dbにデータを入れる
                # for cell in row: 
                #     print(str(cell))      
            # insert_values = [insert_date,"0",price,bucherer_watch_id]
    return jwa_files



# ブヘラ(USA)のデータを統合データベースに入稿する処理

# jwaのデータをデータベースに入稿する処理
def jwa(instance):
    current_directory = os.getcwd()
    folder_name = "まとめるエクセル"
    new_directory = os.path.join(current_directory, folder_name)
    items = instance.tablesdateill
    watch_item_instance = items["watch_item"]
    # 年と月を抽出する正規表現パターン
    yearmonthpattern = re.compile(r'(\d{4})-(\d{2})')
    # フィールドを再定義する。
    # watch_item_instance.fields = ["item_id","ref","year","size","bracelet","dial","url"]
    # insert_values = [insert_date,"0",price,bucherer_watch_id]
    # print(insert_values)
    # watch_item_instance.insert_data(insert_values)
    # JWAファイル取得
    pattern = re.compile(r'^JWA.*\.xlsx$')
    jwa_files = []

    # ディレクトリ内のファイルを走査して、JWAファイルをリストに追加する
    for file in os.listdir(new_directory):
        if pattern.match(file):
            jwa_files.append(os.path.join(new_directory, file))
    # print(jwa_files)
    for file in jwa_files:
        full_path = os.path.join(new_directory, file)
        workbook = load_workbook(full_path, data_only=False)
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            for row in sheet.iter_rows(values_only=True):
                print(list(row))
                rowitemslist = list(row)
                # 週フィールド名
                # weekly_table_fields = ['weekdate','ranking','price','bucherer_watch_id']
                # # 週レポート
                # weekly_report_inset_instance = SQLiteDataInsert(dbname,weekly_table_name,weekly_table_fields)
                insert_values = [rowitemslist[1],"",rowitemslist[16],rowitemslist[10],"","",""]
                insert_values = [rowitemslist[10],"",rowitemslist[16],"","","",""]
                # 
                jwa_make_ID = "JWA-"+str(rowitemslist[1])+"-"+str(rowitemslist[2])+"-"+str(rowitemslist[3])
                yearmonthmatch = yearmonthpattern.match(str(rowitemslist[1]))

                if yearmonthmatch:
                    year = yearmonthmatch.group(1)  # 年の部分を取得
                    month = yearmonthmatch.group(2)  # 月の部分を取得
                    formatted_date = f"{year}/{month}"
                    print(f"Formatted date: {formatted_date}")
                else:
                    print("Date format doesn't match expected pattern.")
                    formatted_date = "noching"
                
                # 品番?
                if rowitemslist[10] is None:
                    # rowitemslist[10] が None の場合の処理
                    print("rowitemslist[10] は None です")
                    ref = "なし"
                else:
                     # rowitemslist[10] が None でない場合の処理
                     print("rowitemslist[10] は None ではありません")
                     ref = rowitemslist[10] 
                    
                # ↓あとで使うやつ
                # ↓その他アイテム
                
                watch_item_instance.insert_data([jwa_make_ID,ref,"","","","","","","JWA",rowitemslist[16],formatted_date,rowitemslist[11]])

                # watch_item_instance.fieldcountAllcountcheck()
                row_data = []
                # dbにデータを入れる
                # for cell in row: 
                #     print(str(cell))      
            # insert_values = [insert_date,"0",price,bucherer_watch_id]
    return jwa_files

def refdatasget(instance):
    items = instance.tablesdateill
    watch_item_instance = items["watch_item"]
    returnitems = watch_item_instance.groupby('test')
    return returnitems


def main():
    today_date = datetime.now().date()
    # エクセルファイル作成
    file_name = f"総合リスト{today_date}.xlsx"

    if not os.path.exists(file_name):
        # Excelブックの作成
        wb = Workbook()
        ws = wb.active
        # ヘッダー行を追加
        ws.append(
            [
             "リファレンス",
             "年代",
             "モデル名",
             "サイズ",
             "ブレスレット",
             "ダイアル",
             "値段"
             ]
    )     
    else:
        # ファイルが存在する場合は既存のファイルを読み込み
        wb = load_workbook(file_name)
        ws = wb.active

    # インスタンスを作成する。
    db_file = "bucherer.db"
    # dbのファイルをわたす。
    whocequeryinstance = WhocheSqliteDataInsert(db_file)
    
    evence(whocequeryinstance)
    return
    jwa(whocequeryinstance)
    return
    # ここで列を指定する。
    excel_alldata = refdatasget(whocequeryinstance) 
    for data in excel_alldata:
        # print(data,"データ一覧")
        ws.append(data)
    wb.save(file_name)

    return
    
    today_date_and_time = datetime.now().strftime("%Y%m%d%H%M%S")
    today_date = datetime.now().strftime("%Y%m%d")
    file_name = f"データ集{today_date}.xlsx"  
    if not os.path.exists(file_name):
        wb = Workbook()
        ws = wb.active
    else:
        wb = load_workbook(file_name)
        ws = wb.active

    current_directory = os.getcwd()
    folder_name = "まとめるエクセル"
    dest_folder = os.path.join(current_directory, f"{folder_name}copy")
    new_directory = os.path.join(current_directory, folder_name)
    
    copy_folder(new_directory, dest_folder)
    excel_files = [file for file in os.listdir(new_directory) if file.endswith('.xlsx') or file.endswith('.xls')]

    Ref_pattern = re.compile(r"\b\d{4,6}[A-Za-z]*\b")

    for file in excel_files:
        full_path = os.path.join(new_directory, file)
        workbook = load_workbook(full_path, data_only=False)
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            for row in sheet.iter_rows(values_only=True):
                row_data = []
                for cell in row:               
                    if cell is not None:
                        Ref_matches = Ref_pattern.findall(str(cell))
                        if Ref_matches:
                            print(Ref_matches,"Ref")
                    row_data.append(cell)
                ws.append(row_data) 
        
        wb.save(file_name)  
        print("Sheets:", wb.sheetnames)

if __name__ == "__main__":
    main()
