import os
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
#import csv
# You can generate an API token from the "API Tokens Tab" in the UI
token = os.getenv("INFLUX_TOKEN")
print(token[:5])
org = "forecasting"
bucket = "energy_consumption"

client = InfluxDBClient(url="http://127.0.0.1:8086", token=token, org=org)

query_api = client.query_api()

query = 'from(bucket:"energy_consumption")' \
        ' |> range(start:2016-10-22T00:00:00Z, stop:2018-10-24T23:45:00Z)'\
        ' |> filter(fn: (r) => r._measurement == "Electric usage")' \
        ' |> filter(fn: (r) => r._field == "usage(KWh)")'

result = query_api.query(org=org, query=query)

data = {'y': [], 'ds': []}

for table in result:
    for record in table.records:
        data['y'].append(record.get_value())
        data['ds'].append(record.get_time())
    print("here")

df = pd.DataFrame(data=data)
print(df.head(20))
#df.to_csv('data/Processed_D202.csv', index=False)

