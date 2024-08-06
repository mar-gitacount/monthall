text = """
SEA DWELLER
DATE
DAYTONA
GMT
DJ
OP
SUB
SUB
DEEP SEA
YACHT
DJ
EX2
EX
DJ
DJ
DD
その他
SKY
DJ
その他
EX
SUB
DJ
YACHT
SUB
DATE
GMT
DJ
GMT
DAYTONA
OP
その他
EX2
SUB
その他
DEEP SEA
SKY
YACHT

"""


# 各アイテムにダブルコーテーションを追加してループ
items_with_quotes = []
for item in text.split("\n"):
    if item.strip():  # 空の行をスキップ
        items_with_quotes.append(f'"{item.strip()}"')

# 結果を出力
for item in items_with_quotes:
    print(item)
