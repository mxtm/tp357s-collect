import argparse
import tomllib
import logging
import signal
import asyncio
from pathlib import Path

from tp357s_collect.db_writer import DBWriter
from tp357s_collect.listener import Listener

logger = logging.getLogger(__name__)

stop_event = asyncio.Event()

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collects (and optionally stores) data from ThermoPro TP357s hygrometers via Bluetooth",
    )

    parser.add_argument(
        "-c",
        "--config-file",
        help="Configuration file in TOML format",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="Display verbose logging",
        action="store_true",
    )

    parser.add_argument(
        "--device-address",
        help="Bluetooth address of TP357S device",
    )

    parser.add_argument(
        "--db-host",
        help="InfluxDB (v1.x) hostname",
    )

    parser.add_argument(
        "--db-port",
        help="InfluxDB (v1.x) port",
        type=int,
    )

    parser.add_argument(
        "--db-username",
        help="InfluxDB (v1.x) username",
    )

    parser.add_argument(
        "--db-password",
        help="InfluxDB (v1.x) password",
    )

    parser.add_argument(
        "--db-name",
        help="InfluxDB (v1.x) database name",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level="DEBUG" if args.verbose else "INFO",
        format='[%(asctime)s] [%(filename)s] [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    config = {
        "device": {
            "address": args.device_address,
        },
        "database": {
            "host": args.db_host,
            "port": args.db_port,
            "username": args.db_username,
            "password": args.db_password,
            "name": args.db_name,
        },
    }

    if args.config_file and (config_path := Path(args.config_file)).exists():
        config = tomllib.loads(config_path.read_text())

    logging.debug(f"Running with config: {config}")

    db_writer = None
    if config["database"]["host"] and config["database"]["port"] and config["database"]["username"] and config["database"]["password"] and config["database"]["name"]:
        db_writer = DBWriter(
            host=config["database"]["host"],
            port=config["database"]["port"],
            username=config["database"]["username"],
            password=config["database"]["password"],
            database=config["database"]["name"],
        )

    signal.signal(signal.SIGINT, lambda x, y: stop_event.set())

    listener = Listener(
        device_address=config["device"]["address"],
        stop_event=stop_event,
        db_writer=db_writer,
    )

    asyncio.run(listener.listen())
