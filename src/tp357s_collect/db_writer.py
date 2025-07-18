import logging
import time

from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)

class DBWriter:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
    ):
        self._client = InfluxDBClient(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
        )

    def write_data(
        self,
        temp_c: float,
        temp_f: float,
        hum: int,
        heat_index: float,
    ):
        current_time = time.time_ns()

        formatted_data = [
            {
                "measurement": "temperature",
                "tags": {},
                "time": current_time,
                "fields": {
                    "fahrenheit": temp_f,
                    "celsius": temp_c,
                },
            },
            {
                "measurement": "humidity",
                "tags": {},
                "time": current_time,
                "fields": {
                    "relative": hum,
                },
            },
            {
                "measurement": "heat_index",
                "tags": {},
                "time": current_time,
                "fields": {
                    "value": heat_index,
                },
            },
        ]

        self._client.write_points(formatted_data)
