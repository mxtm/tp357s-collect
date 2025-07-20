import asyncio
import logging

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tp357s_collect.parser import parse_raw_tp357s_gatt_data
from tp357s_collect.converters import (
    convert_celsius_to_fahrenheit,
    get_heat_index,
)
from tp357s_collect.db_writer import DBWriter

logger = logging.getLogger(__name__)

CHARACTERISTIC_UUID = "00010203-0405-0607-0809-0a0b0c0d2b10"

class Listener:
    def __init__(
        self,
        device_address: str,
        stop_event: asyncio.Event,
        db_writer: DBWriter | None = None,
    ) -> None:
        self._device_address = device_address
        self._stop_event = stop_event
        self._db_writer = db_writer

    async def listen(self) -> None:
        async with BleakClient(self._device_address) as client:
            await client.start_notify(CHARACTERISTIC_UUID, self.handle_notification)
            await self._stop_event.wait()
            await client.stop_notify(CHARACTERISTIC_UUID)

    def handle_notification(
        self,
        sender: BleakGATTCharacteristic,
        data: bytearray,
    ) -> None:
        parsed_data = parse_raw_tp357s_gatt_data(data)

        temp_f = round(
            convert_celsius_to_fahrenheit(parsed_data.temp_c),
            2,
        )

        heat_index = get_heat_index(temp_f, parsed_data.hum)

        logger.info(f"Temp: {parsed_data.temp_c} C / {temp_f} F")
        logger.info(f"Humidity: {parsed_data.hum}%")
        logger.info(f"Heat Index: {heat_index} F")

        if self._db_writer:
            self._db_writer.write_data(
                temp_c=parsed_data.temp_c,
                temp_f=temp_f,
                hum=parsed_data.hum,
                heat_index=heat_index,
            )
