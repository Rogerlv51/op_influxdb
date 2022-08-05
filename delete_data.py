from influxdb_client import InfluxDBClient

url="http://192.168.1.51:32716"
token="m9nBYCOJ70_sSn5wDt9EyQfSSWDX4mjAGMt27-d2cF0d_BJsnRML5czj40_IOSW6IS1Uahm5eg0C2Io2QAmENw=="
org="unianalysis"
client = InfluxDBClient(url=url, token=token, timeout=1000000000)

delete_api = client.delete_api()

"""
Delete Data
"""
start = "1690-01-01T00:00:00Z"
stop = "2022-08-05T00:00:00Z"
delete_api.delete(start, stop, '_measurement="tourism_all"', bucket='standard', org=org)

"""
Close client
"""
client.close()