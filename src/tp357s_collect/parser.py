import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ParsedTP357SData:
    temp_c: float
    hum: int

def parse_raw_tp357s_gatt_data(data: bytearray) -> ParsedTP357SData:
    logger.debug(f"Raw data received: {data.hex()}")
    return ParsedTP357SData(
        temp_c=data[3] / 10.0,
        hum=data[5],
    )
