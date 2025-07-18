# TP357S Collect

A tool that listens to GATT notifications broadcast by ThermoPro TP357S hygrometers, and optionally saves this data to InfluxDB.

Can either be configured using a TOML configuration file in the format in `example_config.toml`, or configured through command line options.

All the other options that I found for parsing and recording this data had at least one fatal flaw for my use case.

More functionality (like reading historical data stored on device) may be added. Any contributions are welcome!
