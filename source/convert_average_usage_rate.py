import json
import pandas as pd

parking_names = [
    "中央駐車場",
    "南部駐車場",
    "美術館地下駐車場",
    "杣場川駐車場",
    "瓦町駅地下駐車場",
    "サンポート高松地下駐車場",
    "高松駅前広場地下駐車場",
    "高松シンボルタワー地下駐車場",
    "高松駅南交通広場駐車場",
]


weekday_df = pd.read_csv("weekdayUsageRate.csv", encoding="utf-8")
holiday_df = pd.read_csv("holidayUsageRate.csv", encoding="utf-8")

parking_usage_data = []

for name in parking_names:

    weekday_usage = [
        {"time": row["平日"], "rate": row[name]} for _, row in weekday_df.iterrows()
    ]

    holiday_usage = [
        {"time": row["休日"], "rate": row[name]} for _, row in holiday_df.iterrows()
    ]

    # Create the final structure
    parking_usage_data.append(
        {
            "name": name,
            "averageUsageRateWeekday": weekday_usage,
            "averageUsageRateHoliday": holiday_usage,
        }
    )

with open("parking_usage_data.json", "w", encoding="utf-8") as f:
    json.dump(parking_usage_data, f, indent=4, ensure_ascii=False)
