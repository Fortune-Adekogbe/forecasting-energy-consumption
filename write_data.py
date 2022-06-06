from datetime import datetime, date, time
import os, pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
#import csv
# You can generate an API token from the "API Tokens Tab" in the UI
token = os.getenv("INFLUX_TOKEN")

org = "forecasting"
bucket = "energy_consumption"

client = InfluxDBClient(url="http://127.0.0.1:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

df = pd.read_csv('data/D202.csv')
print(df.head(20))

print(df.dtypes)
for index, row in df.iterrows():
    print(index, end=' ')
    stamp = datetime.strptime(f"{row['DATE']}, {row['START TIME']}", 
                                "%m/%d/%Y, %H:%M")
    p = Point(row["TYPE"])\
        .time(stamp, WritePrecision.NS)\
        .field("usage(KWh)", row["USAGE"])\
        .tag("cost", row["COST"])
        # .tag("end_time", f"{row['DATE']}, {row['END TIME']}")\
    write_api.write(bucket=bucket, org=org, record=p)
    if index == 10000:
        break
        




# query_api = client.query_api()

# query = 'from(bucket:"energy_consumption")' \
#         ' |> range(start:2022-05-18T14:14:00Z, stop:2022-05-18T14:14:50Z)'\
#         ' |> filter(fn: (r) => r._measurement == "measurement1")' \
#         ' |> filter(fn: (r) => r._field == "field1")'

# result = query_api.query(org=org, query=query)

# raw = []
# for table in result:
#     for record in table.records:
#         raw.append((record.get_value(), record.get_time()))
# print(raw[0:5])