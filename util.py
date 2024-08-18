from datetime import datetime, time, timedelta
from dateutil.relativedelta import relativedelta
import json
import random
import pandas as pd


def write_json(output: dict, file_name: str):
    with open(f"result/{file_name}.json", "w") as f:
        json.dump(output, f, indent=4)


def append_json_data(append_data_list: list, file_name: str):
    with open(f"result/{file_name}.json", "r") as f:
        data = json.load(f)
        data["records"].extend(append_data_list)
        write_json(data, file_name)


def parking_average_usage_rate(parking_name: str) -> tuple:
    with open(f"parkingLot/{parking_name}.json") as f:
        json_data = json.load(f)
        return (
            json_data["averageUsageRateWeekday"],
            json_data["averageUsageRateHoliday"],
        )


def parking_open_time(parking_name: str) -> time:
    with open(f"parkingLot/{parking_name}.json") as f:
        return datetime.strptime(json.load(f)["openTime"], "%H:%M:%S").time()


def parking_close_time(parking_name: str) -> time:
    with open(f"parkingLot/{parking_name}.json") as f:
        return datetime.strptime(json.load(f)["closeTime"], "%H:%M:%S").time()


def is_alltime_open(parking_name: str) -> bool:
    return parking_open_time(parking_name) == parking_close_time(parking_name)


def parking_capacity(parking_name: str) -> int:
    with open(f"parkingLot/{parking_name}.json") as f:
        return json.load(f)["capacity"]


def parking_category(parking_name: str) -> str:
    with open(f"parkingLot/{parking_name}.json") as f:
        return json.load(f)["category"]


# def filtered_weather_data(datetime: datetime) -> pd.DataFrame:
#     df = pd.read_csv("source/weatherData.csv")
#     df["DateTime"] = pd.to_datetime(df["DateTime"])
#     return df[df["DateTime"].dt.date == datetime.date()]


def weather_data(datetime: datetime) -> pd.DataFrame:
    df = pd.read_csv("source/weatherData.csv")
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    weather_data_df = df[df["DateTime"] == datetime]
    if len(weather_data_df) != 1:
        raise ValueError("No weather data found or over length")
    return weather_data_df


def event_rate(datetime: datetime) -> float:
    datetime += relativedelta(
        years=1
    )  # TODO: 今年を模倣するためダミーは一年前でもイベントは今年を使うため一年足してずらす
    df = pd.read_json("source/eventData.json")
    df["startDateTime"] = pd.to_datetime(df["startDateTime"])
    df["endDateTime"] = pd.to_datetime(df["endDateTime"])

    event_data_df = df[
        (df["startDateTime"] <= datetime) & (datetime <= df["endDateTime"])
    ]

    if len(event_data_df) > 1:
        raise ValueError("Event Over length")
    if len(event_data_df) == 0:
        return 0

    return event_data_df["rate"].iloc[0]


def get_day_of_week(date):
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    weekday_index = date.weekday()

    return weekdays[weekday_index]


def datetime_average_usage_rate(datetime: datetime, parking_name: str):
    day_of_week = get_day_of_week(datetime)

    weekday_average_usage_rates, holiday_average_usage_rates = (
        parking_average_usage_rate(parking_name)
    )

    if day_of_week == "Sunday" or day_of_week == "Saturday":
        average_usage_rates = holiday_average_usage_rates
    else:
        average_usage_rates = weekday_average_usage_rates
    average_usage_rate = next(
        (
            item["rate"]
            for item in average_usage_rates
            if item["time"] == datetime.time().strftime("%H:%M:%S")
        ),
        None,
    )
    if average_usage_rate is None:
        raise ValueError("No average usage rate data found")

    return average_usage_rate


def calc_usage_rate(datetime: datetime, parking_name: str):
    """
    時間帯の平均利用率の計算(平均利用率 + 天候データ + イベントデータ)
    """
    # 平均利用率の取得
    average_usage_rate = datetime_average_usage_rate(datetime, parking_name)

    # 天候による変動率(%)の取得
    weather_data_df = weather_data(datetime)
    weather_rate = int(weather_data_df["WeatherScale"].iloc[0])

    # イベントによる変動率(%)の取得
    event_rate_data = event_rate(datetime)

    average_usage_rate += weather_rate + event_rate_data

    if average_usage_rate < 0:
        # 念の為
        print(f"Usage rate is negative: {datetime}")
        print(f"average rate: {average_usage_rate}")
        print(f"weather rate: {weather_rate}")
        print(f"event rate: {event_rate_data}")
        average_usage_rate = 1  # 最終的な平均利用率が0にならないようにする

    return average_usage_rate


def is_time_overlap(entry_time, exit_time, target_datetime):
    # target_datetime から1時間後の時間を計算
    target_end_time = target_datetime + timedelta(hours=1)

    # 判定: 区間が重なっているかどうか
    return entry_time <= target_end_time and exit_time >= target_datetime


def usage_data(parking_name: str):
    with open(f"result/{parking_name}.json") as f:
        json_data = json.load(f)
        return json_data


def usage_car_count(records, datetime: datetime):
    count = 0
    for record in records:
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])
        if is_time_overlap(entry_time, exit_time, datetime):
            count += 1
    return count


def datetime_diff_min(datetime1, datetime2):
    difference = datetime2 - datetime1
    return difference.total_seconds() / 60


def generate_entry_time(current_datetime: datetime):
    entry_limit_time = current_datetime + timedelta(minutes=30)
    entry_time_range = datetime_diff_min(current_datetime, entry_limit_time)
    entry_time = current_datetime + timedelta(
        minutes=int(random.uniform(0, entry_time_range))
    )

    return entry_time


def generate_dates_for_one_year(start_date_str):
    start_date = datetime.strptime(start_date_str, "%Y")

    dates = []

    for i in range(365):
        current_date = start_date + timedelta(days=i)
        dates.append(
            current_date.strftime("%Y-%m-%d")
        )  # "YYYY-MM-DD"形式でリストに追加

    return dates


def get_dates(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # 日付リストを作成
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return date_list
