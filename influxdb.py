
'''
from collections import OrderedDict
from csv import DictReader

import reactivex as rx
from reactivex import operators as ops

from influxdb_client import InfluxDBClient, Point, WriteOptions

def parse_row(row: OrderedDict):
    """Parse row of CSV file into Point with structure:

        financial-analysis,type=ily close=18.47,high=19.82,low=18.28,open=19.82 1198195200000000000

    CSV format:
        Date,VIX Open,VIX High,VIX Low,VIX Close\n
        2004-01-02,17.96,18.68,17.54,18.22\n
        2004-01-05,18.45,18.49,17.44,17.49\n
        2004-01-06,17.66,17.67,16.19,16.73\n
        2004-01-07,16.72,16.75,15.5,15.5\n
        2004-01-08,15.42,15.68,15.32,15.61\n
        2004-01-09,16.15,16.88,15.57,16.75\n
        ...

    :param row: the row of CSV file
    :return: Parsed csv row to [Point]
    """

    """
     For better performance is sometimes useful directly create a LineProtocol to avoid unnecessary escaping overhead:
     """
     # from datetime import timezone
     # import ciso8601
     # from influxdb_client.client.write.point import EPOCH
     #
     # time = (ciso8601.parse_datetime(row["Date"]).replace(tzinfo=timezone.utc) - EPOCH).total_seconds() * 1e9
     # return f"financial-analysis,type=vix-daily" \
     #        f" close={float(row['VIX Close'])},high={float(row['VIX High'])},low={float(row['VIX Low'])},open={float(row['VIX Open'])} " \
     #        f" {int(time)}"

    return Point("new_uci") \
        .tag("_field", row['_field']) \
        .tag("custom", row['custom']) \
        .field("_value", float(row['_value'])) \
        .time(row['datetime'])
    # tag 是用来检索的

"""
Converts vix-daily.csv into sequence of datad point
"""
data = rx \
    .from_iterable(DictReader(open('final.csv', 'r'))) \
    .pipe(ops.map(lambda row: parse_row(row)))

client = InfluxDBClient(url="http://4k377z0213.zicp.vip:53547", 
                        token="m9nBYCOJ70_sSn5wDt9EyQfSSWDX4mjAGMt27-d2cF0d_BJsnRML5czj40_IOSW6IS1Uahm5eg0C2Io2QAmENw==", 
                        org="unianalysis", debug=True)

"""
Create client that writes data in batches with 50_000 items.
"""
write_api = client.write_api(write_options=WriteOptions(batch_size=50_000, flush_interval=10_000))

"""
Write data into InfluxDB
"""
write_api.write(bucket="standard", record=data)
write_api.close()

"""
Querying max value of CBOE Volatility Index
"""
query = 'from(bucket:"standard")' \
        ' |> range(start: 0, stop: now())' \
        ' |> filter(fn: (r) => r._measurement == "new_uci")' \
        ' |> max()'
result = client.query_api().query(query=query)

"""
Processing results
"""
print()
print("=== results ===")
print()
for table in result:
    for record in table.records:
        print('max {0:5} = {1}'.format(record.get_field(), record.get_value()))

"""
Close client
"""
client.close()
'''

from datetime import datetime, timedelta

import pandas as pd
import reactivex as rx
from reactivex import operators as ops

from influxdb_client import InfluxDBClient, Point, WriteOptions

with InfluxDBClient(url="http://4k377z0213.zicp.vip:53547", token="m9nBYCOJ70_sSn5wDt9EyQfSSWDX4mjAGMt27-d2cF0d_BJsnRML5czj40_IOSW6IS1Uahm5eg0C2Io2QAmENw==", org="unianalysis") as _client:

    with _client.write_api(write_options=WriteOptions(batch_size=5000000,
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
        _data_frame = pd.read_csv("final.csv")

        _write_client.write("standard", "unianalysis", record=_data_frame, data_frame_measurement_name='new_uci',
                            data_frame_tag_columns=['_field', 'custom'])