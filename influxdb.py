
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import reactivex as rx
from reactivex import operators as ops

from influxdb_client import InfluxDBClient, Point, WriteOptions

ts = pd.date_range('2012-01-01 00:00:01', freq='1H', periods=26304, tz="Asia/Shanghai")
#ts = pd.Series(ts)
print(ts)
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
df_2 = df_1.melt(var_name="custom", value_name="ele_load")
df_2.index = ts
df_2["ele_load"] = df_2["ele_load"].astype('float')
print(df_2)
# df_3 = pd.concat([ts, df_2], axis=1)
# df_3.rename(columns={0: "datetime"}, inplace=True)
#df_3.rename(columns={"elec_load": "_value"}, inplace=True)
#list2 = []
#str = "ele_load"
#for item in range(8443584):
    #list2.append(str)
#df_3["_field"] = list2
# df_3.to_csv("final.csv", index=None)
# df_3.to_csv("final.csv", index=None)
# print(df_2)

with InfluxDBClient(url="http://192.168.1.51:32716", token="m9nBYCOJ70_sSn5wDt9EyQfSSWDX4mjAGMt27-d2cF0d_BJsnRML5czj40_IOSW6IS1Uahm5eg0C2Io2QAmENw==", org="unianalysis") as _client:

    with _client.write_api(write_options=WriteOptions(batch_size=1000,
                                                      flush_interval=10_000,
                                                      jitter_interval=2_000,
                                                      retry_interval=5_000,
                                                      max_retries=5,
                                                      max_retry_delay=30_000,
                                                      exponential_base=2)) as _write_client:


        """
        Write Pandas DataFrame
        """
        # _now = datetime.utcnow()
        # _data_frame = pd.read_csv("final.csv")

        _write_client.write("standard", "unianalysis", record=df_2, data_frame_measurement_name='uci_hourly',
                            data_frame_tag_columns=['custom'])