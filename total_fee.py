import json

parking_name = "中央駐車場"
h25_total = 79343000  # 中央駐車場のH25年度の総収入

with open(f"result/{parking_name}-price.json", "r") as f:
    data = json.load(f)

total_price = sum(item["price"] for item in data)
max_fee = max(item["price"] for item in data)
min_fee = min(item["price"] for item in data)
unique_price = set(item["price"] for item in data)

print(f"H25 Total: {h25_total}")
print(f"Total    : {total_price}")
print(f"Diff Rata: {total_price / h25_total}")
print(f"Max      : {max_fee}")
print(f"Min      : {min_fee}")
print(f"Unique   : {unique_price}")
