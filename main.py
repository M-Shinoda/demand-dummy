from datetime import datetime
from simulate import generate_parking_records
from util import generate_dates_for_one_year, get_dates, write_json


parking_name = "中央駐車場"

# # 1年間のデータを生成
# dates = generate_dates_for_one_year("2023")
# for date in dates:
#     parking_data = generate_parking_records(parking_name, date)
#     output = {"records": parking_data}
#     write_json(output, f"{parking_name}")

# # 特定日のデータを生成
# parking_data = generate_parking_records(parking_name, "2023-01-01")
# output = {"records": parking_data}
# write_json(output, f"{parking_name}")

# 特定範囲のデータを生成
dates = get_dates("2023-11-28", "2023-12-31")
# dates = [
#     "2023-01-01",
#     "2023-01-02",
#     "2023-01-03",
#     "2023-01-04",
#     "2023-01-05",
#     "2023-01-06",
#     "2023-01-07",
#     "2023-01-08",
# ]

for date in dates:
    parking_data = generate_parking_records(parking_name, date)
    output = {"records": parking_data}
    write_json(output, f"{parking_name}")
