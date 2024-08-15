import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# JSONデータの読み込み
with open("result/中央駐車場.json") as f:
    data = json.load(f)

# フィルタリングしたい期間を設定
start_time = pd.to_datetime("2023-01-04T19:00:00+09:00")
end_time = pd.to_datetime("2023-01-07T07:30:00+09:00")

df = pd.DataFrame(data["records"])

df["entryTime"] = pd.to_datetime(df["entryTime"])
df["exitTime"] = pd.to_datetime(df["exitTime"])

filtered_df = df.loc[(df["entryTime"] >= start_time) & (df["entryTime"] <= end_time)]

plt.figure(figsize=(10, 6))

for i in range(len(filtered_df)):
    plt.plot(
        [filtered_df["entryTime"].iloc[i], filtered_df["exitTime"].iloc[i]],
        [i, i],
        color="blue",
        linewidth=10,
    )

plt.xlabel("Time")
plt.ylabel("Index")
plt.title("Entry and Exit Times")
plt.grid(True)
plt.yticks(range(len(filtered_df)), filtered_df.index)
plt.xticks(rotation=45)

plt.show()
