
from influxdb_client import InfluxDBClient, Point, WriteOptions
bucket = "standard"
org = "unianalysis"
token = "m9nBYCOJ70_sSn5wDt9EyQfSSWDX4mjAGMt27-d2cF0d_BJsnRML5czj40_IOSW6IS1Uahm5eg0C2Io2QAmENw=="
# Store the URL of your InfluxDB instance
url="http://4k377z0213.zicp.vip:53547"

import pandas as pd
import numpy as np

data = pd.read_csv("toursim_final.csv")
df_1 = data.iloc[139624:,:]
df_1.index = df_1['time']
df_1.to_csv('tourism_year.csv', index=None)
print(df_1)


'''
with InfluxDBClient(url=url, token=token, org=org) as _client:

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

        _write_client.write("standard", "unianalysis", record=df_1, data_frame_measurement_name='tourism_year',
                            data_frame_tag_columns=['landscape'])
'''