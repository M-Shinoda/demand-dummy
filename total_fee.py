import json

parking_name = "中央駐車場"

with open(f"result/{parking_name}-price.json", "r") as f:
    data = json.load(f)

total_price = sum(item["price"] for item in data)

print(f"Total Price: {total_price}")
