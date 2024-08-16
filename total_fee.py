import json

h25_total_by_paking_name = {
    "中央駐車場": 79343000,
    "南部駐車場": 25472000,
    "美術館地下駐車場": 46706000,
    "杣場川駐車場": 20576000,
    "瓦町駅地下駐車場": 102780000,
    # "サンポート高松地下駐車場":,
    "高松駅前広場地下駐車場": 108598000,
    "高松シンボルタワー地下駐車場": 38893000,
    "高松駅南交通広場駐車場": 4118000,
}


def total_fee(parking_name):
    with open(f"result/{parking_name}-price.json", "r") as f:
        data = json.load(f)

    total_price = sum(item["price"] for item in data)
    max_fee = max(item["price"] for item in data)
    min_fee = min(item["price"] for item in data)
    unique_price = set(item["price"] for item in data)

    h25_total = h25_total_by_paking_name[parking_name]

    print(f"H25 Total : {h25_total}")
    print(f"Total     : {total_price}")
    print(f"Match Rate: {total_price / h25_total}")
    print(f"Max       : {max_fee}")
    print(f"Min       : {min_fee}")
    print(f"Unique    : {unique_price}")


if __name__ == "__main__":
    parking_name = "中央駐車場"
    total_fee(parking_name)
