"""
a2sensor/sensor_collect/sensor_collect.py

This script runs Sensor-Collect.

Copyright (C) 2023-today a2sensor's a2sensor/sensor_collect

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from .server import Server
import os

def configure_from_cli():
    """
    Configures the Server based on the CLI arguments.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Runs this server to read values from attached sensors"
    )
    parser.add_argument("-d", "--data-folder", required=True, help="The data folder")
    parser.add_argument(
        "-c",
        "--local-sensors-config-file",
        required=True,
        help="The configuration file for the attached sensors",
    )
    args, unknown_args = parser.parse_known_args()
    Server.configure(args.data_folder, args.local_sensors_config_file)

if __name__ == "__main__":
    configure_from_cli()
    Server.instance().local_sensors.start()
else:
    Server.configure()
