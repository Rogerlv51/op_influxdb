from influxdb_client import InfluxDBClient, Point, Dialect
bucket = "standard"
org = "unianalysis"
token = "m9nBYCOJ70_sSn5wDt9EyQfSSWDX4mjAGMt27-d2cF0d_BJsnRML5czj40_IOSW6IS1Uahm5eg0C2Io2QAmENw=="
# Store the URL of your InfluxDB instance
url="http://192.168.1.51:32716"

import pandas as pd
import numpy as np

data = pd.read_csv("tourism.csv")
print(data.info)