from datetime import datetime, timedelta
import json
import pytz
import matplotlib.pyplot as plt

from util import is_time_overlap

timezone = pytz.timezone("Asia/Tokyo")

parking_name = "中央駐車場"
# 初期のtarget_datetimeを設定
start_datetime = datetime(2023, 1, 1, 0, 0, 0)
start_datetime = timezone.localize(start_datetime)
end_datetime = datetime(2023, 1, 1, 23, 59, 0)
end_datetime = timezone.localize(end_datetime)
#

with open(f"result/{parking_name}.json") as f:
    data = json.load(f)


times = []
counts = []

current_datetime = start_datetime
while current_datetime < end_datetime:
    print(current_datetime)
    count = 0
    for record in data["records"]:
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])

        if is_time_overlap(entry_time, exit_time, current_datetime):
            count += 1

    times.append(current_datetime.strftime("%Y-%m-%d %H:%M"))
    counts.append(count)

    current_datetime += timedelta(hours=1)

# グラフの描画
plt.figure(figsize=(20, 10))
plt.plot(times, counts, marker="o", markersize=2)
plt.title("Number of Overlapping Records by Time (1 Year)")
plt.xlabel("Time")
plt.ylabel("Number of Overlapping Records")
plt.grid(True)
plt.xticks(rotation=90, fontsize=8)
plt.show()
