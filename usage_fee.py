import json
from datetime import datetime, timedelta
import math

import pytz

from util import get_day_of_week

parking_name = "中央駐車場"
timezone = pytz.timezone("Asia/Tokyo")


# JSONファイルを読み込み
with open(f"result/{parking_name}.json", "r") as f:
    usage_data = json.load(f)


def get_pricing_type(datetime):
    day_of_week = get_day_of_week(datetime)
    if day_of_week == "Saturday" or day_of_week == "Sunday":
        return "holiday"
    else:
        return "weekday"


def pricing_at_entry(current_time, pricing):
    timezone = pytz.timezone("Asia/Tokyo")
    section_start_datetime = datetime.strptime(
        f'{current_time.strftime("%Y-%m-%d")} {pricing["start"]}',
        "%Y-%m-%d %H:%M:%S",
    )
    section_start_datetime = timezone.localize(section_start_datetime)
    if (
        datetime.strptime(pricing["start"], "%H:%M:%S").time()
        > datetime.strptime(pricing["end"], "%H:%M:%S").time()
    ):
        next_daty = current_time + timedelta(days=1)
        section_end_datetime = datetime.strptime(
            f'{next_daty.strftime("%Y-%m-%d")} {pricing["end"]}',
            "%Y-%m-%d %H:%M:%S",
        )
    else:
        section_end_datetime = datetime.strptime(
            f'{current_time.strftime("%Y-%m-%d")} {pricing["end"]}',
            "%Y-%m-%d %H:%M:%S",
        )
    section_end_datetime = timezone.localize(section_end_datetime)

    return section_start_datetime, section_end_datetime


def unit_price(parking_name, entry_time, exit_time):
    with open(f"parkingLot/{parking_name}.json", "r") as f:
        lot_info = json.load(f)

    current_time = entry_time
    total_price = 0

    while current_time < exit_time:
        pricing_type_filter = list(
            filter(
                lambda x: x["type"] == get_pricing_type(current_time),
                lot_info["pricingModel"],
            )
        )
        for pricing in pricing_type_filter:
            start, end = pricing_at_entry(current_time, pricing)

            # print(f"start: {start}")
            # print(f"end: {end}")
            # print(current_time)

            if start <= current_time < end:
                if exit_time > end:
                    price = (
                        math.ceil(
                            (end - current_time).total_seconds()
                            / 60
                            / pricing["intervalMin"]
                        )
                        * pricing["additionalPrice"]
                    )
                    current_time = end
                else:
                    price = (
                        math.ceil(
                            (exit_time - current_time).total_seconds()
                            / 60
                            / pricing["intervalMin"]
                        )
                        * pricing["additionalPrice"]
                    )
                    current_time = exit_time

                if pricing["fixedPrice"] is not None and price >= pricing["fixedPrice"]:
                    total_price += pricing["fixedPrice"]
                else:
                    total_price += price

                break
    return total_price


if __name__ == "__main__":
    # 各車両の利用料金を計算
    results = []
    for record in usage_data["records"]:
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])
        price = unit_price(parking_name, entry_time, exit_time)
        results.append(
            {
                "id": record["id"],
                "entryTime": record["entryTime"],
                "exitTime": record["exitTime"],
                "price": price,
            }
        )

    # 結果を表示
    for result in results:
        print(
            f"ID: {result['id']}, Entry Time: {result['entryTime']}, Exit Time: {result['exitTime']}, Price: {result['price']}"
        )

    with open(f"result/{parking_name}-price.json", "w") as f:
        json.dump(results, f, indent=4)
