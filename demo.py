# from influxdb import InfluxDBClient

from operator import index
import influxdb_client
import pandas as pd
import numpy as np

bucket = "standard"
org = "unianalysis"
token = "m9nBYCOJ70_sSn5wDt9EyQfSSWDX4mjAGMt27-d2cF0d_BJsnRML5czj40_IOSW6IS1Uahm5eg0C2Io2QAmENw=="
# Store the URL of your InfluxDB instance
url="http://192.168.1.51:32716"

'''
data = pd.read_csv("electricity_hourly_dataset.ts", header=None)
df1 = data.iloc[:,0].str.split(":")
df2 = data.iloc[:,1:]
df = pd.concat([df1, df2], axis=1)
df["26304"] = df.iloc[:,0].str[0]
df3 = df.iloc[:, 1:-1]
df4 = df["26304"]
df5 = df.iloc[:,0].str[2]
df6 = pd.concat([df5, df3, df4], axis=1)
print(df6)
df6.to_csv("test.csv", index=None)
'''

ts = pd.date_range('2012-01-01 00:00:01', freq='1H', periods=26304)
#ts = pd.Series(ts)
ts = np.tile(ts, 321)   # 复制所有时间列，对应到不同的custom
ts = pd.Series(ts)

df = pd.read_csv("test.csv",index_col=None)
# print(df)
df = df.T
df_1 = df.iloc[0:-1,:]

list = []
for item in range(321):
    temp = "T" + str(item+1)
    list.append(temp)

df_1.columns = list

# print(df_1)
df_2 = df_1.melt(var_name="custom", value_name="elec_load")
df_3 = pd.concat([ts, df_2], axis=1)
df_3.rename(columns={0: "datetime"}, inplace=True)
df_3.rename(columns={"elec_load": "_value"}, inplace=True)
list2 = []
str = "ele_load"
for item in range(8443584):
    list2.append(str)
df_3["_field"] = list2
# df_3.to_csv("final.csv", index=None)
df_3.to_csv("final.csv", index=None)
print(df_3)