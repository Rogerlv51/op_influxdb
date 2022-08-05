import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient, Point, WriteOptions

df = pd.read_csv("m4.csv")
df_1 = df.iloc[6184:,:]

ts = pd.date_range('1694-12-31 00:00:00', freq='Y', periods=325, tz="Asia/Shanghai")
ts = np.tile(ts, 2)   # 复制所有时间列，对应到不同的custom
ts = pd.Series(ts)
print(ts)
df_1.index = ts

print(df_1)
# print(df.iloc[6184,:])



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

        _write_client.write("standard", "unianalysis", record=df_1, data_frame_measurement_name='m4_year',
                            data_frame_tag_columns=['series'])

