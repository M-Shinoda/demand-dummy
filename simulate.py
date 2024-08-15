import random
import uuid
from datetime import datetime, timedelta

import pytz

from util import (
    calc_usage_rate,
    generate_entry_time,
    is_alltime_open,
    parking_capacity,
    parking_category,
    parking_close_time,
    parking_open_time,
    usage_car_count,
    usage_data,
)


category_by_usage_average_hour = {"working": 1, "entertainment": 3, "both": 2}
category_usage_average_min_sigma = 15


def generate_parking_records(parking_name, date_str):
    records = usage_data(parking_name)["records"]

    current_date = datetime.strptime(date_str, "%Y-%m-%d")
    timezone = pytz.timezone("Asia/Tokyo")
    current_date = timezone.localize(current_date)

    for i in range(24):
        current_datetime = current_date + timedelta(hours=i)

        # TODO:
        # 　営業時間内か判定(1時間ごと)
        if current_datetime.time() < parking_open_time(
            parking_name
        ) or current_datetime.time() >= parking_close_time(parking_name):
            # 30分追加して30分後の時間には営業しているか判定
            add_half_hour_current_datetime = current_datetime + timedelta(minutes=30)
            if add_half_hour_current_datetime.time() == parking_open_time(parking_name):
                current_datetime = add_half_hour_current_datetime
                # print(f"{current_datetime}")
            else:
                # print(f"{current_datetime}: out of time")
                continue
        else:
            print(current_datetime)
            pass
        # TODO: ここまで

        # replace(minute=0)は営業開始が30分の場合があるため、rateのリストで見つからないので3minを0に設定
        usage_rate = calc_usage_rate(current_datetime.replace(minute=0), parking_name)

        usage_car_by_rate = parking_capacity(parking_name) * usage_rate / 100

        use_car_count = usage_car_count(records, current_datetime.replace(minute=0))

        incoming_cars = round(usage_car_by_rate - use_car_count)

        # 車両の入庫と滞在時間の設定
        for _ in range(incoming_cars):
            entry_time = generate_entry_time(current_datetime)
            category_usage_average_hour = category_by_usage_average_hour[
                parking_category(parking_name)
            ]
            exit_time = entry_time + timedelta(
                minutes=int(
                    random.gauss(
                        category_usage_average_hour * 60,
                        category_usage_average_min_sigma,
                    )
                )
            )

            close_time = parking_close_time(parking_name)
            close_datetime = datetime.combine(current_date.date(), close_time)
            close_datetime = timezone.localize(close_datetime)
            # 条件を確認して差分を取得
            if not is_alltime_open(parking_name) and exit_time >= close_datetime:
                difference = exit_time - close_datetime
                # 駐車場が閉まる時間を超えていた場合、翌日の開始時間+残りの差分をにexit_time設定
                if not (
                    exit_time.date() - entry_time.date() >= timedelta(days=1)
                ):  # exit_timeがすでに翌日の場合はそのまま
                    exit_time += timedelta(days=1)
                exit_time = datetime.combine(
                    exit_time.date(), parking_open_time(parking_name)
                )
                exit_time += difference
                exit_time = timezone.localize(exit_time)

            records.append(
                {
                    "id": str(uuid.uuid4()),
                    "entryTime": entry_time.isoformat("T"),
                    "exitTime": exit_time.isoformat("T"),
                }
            )

    return records
