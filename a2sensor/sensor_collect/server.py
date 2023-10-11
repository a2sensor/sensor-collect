"""
a2sensor/sensor_collect/server.py

This script defines the Server class.

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
from datetime import datetime
from flask import Flask, request, jsonify
import json
import logging
import os
import socket
import sys
import threading
from typing import Dict

class Server():
    """
    Represents a Server that collects data from sensors.

    Class name: Server

    Responsibilities:
        - Collect data from sensors.

    Collaborators:
        - None
    """
    _instance = None

    def __init__(self, storageFolder:str, udpPort:int=None, localSensorsConfig:str=None):
        """
        Creates a new Server instance.
        :param storageFolder: The folder to store measures.
        :type storageFolder: str
        :param udpPort: The UDP port.
        :type udpPort: int
        :param localSensorsConfig: The configuration file specifying the local sensors. Optional
        :type localSensorsConfig: bool
        """
        super().__init__()
        self._storage_folder = storageFolder
        self._udp_port = udpPort
        self._local_sensors_config = localSensorsConfig

        if not os.path.exists(self._storage_folder):
            os.makedirs(self._storage_folder)  # create the folder if it doesn't exist

        if udpPort is not None:
            threading.Thread(target=udpPort).start()

        if localSensorsConfig:
            from .local_sensors import LocalSensors
            self._local_sensors = LocalSensors(localSensorsConfig, self.save_to_file)

    @property
    def storage_folder(self):
        """
        Retrieves the storage folder.
        :return: Such value.
        :rtype: str
        """
        return self._storage_folder

    @property
    def udp_port(self):
        """
        Retrieves the UDP port.
        :return: Such port.
        :rtype: int
        """
        return self._udp_port

    @property
    def local_sensors_config(self) -> str:
        """
        Retrieves the location of the configuration file for the local sensors, if any.
        :return: The path of the configuration file.
        :rtype: str
        """
        return self._local_sensors_config

    @property
    def local_sensors(self):
        """
        Retrieves the LocalSensors reference.
        :return: Such instance.
        :rtype: a2sensor.sensor_collect.LocalSensors
        """
        return self._local_sensors

    def save_to_file(self, sensorId:str, sensorName:str, status:str):
        """
        Saves given measure to disk.
        :param sensorId: The id of the sensor.
        :type sensorId: str
        :param sensorName: The sensor name.
        :type sensorName: str
        :param status: The status the sensor has read.
        :type status: str
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        data = {}
        data['id'] = sensorId
        data['name'] = sensorName
        value = {}
        value['status'] = status
        value['timestamp'] = timestamp
        data['value'] = value

        logging.getLogger("a2sensor").info(f"New data from sensor {sensorId}: {data}")
        folder = os.path.join(self.storage_folder, sensorId)
        if not os.path.exists(folder):
            os.makedirs(folder)

        filepath = os.path.join(folder, f"{timestamp}.json")

        with open(filepath, 'w') as file:
            json.dump(data, file)

    @classmethod
    def configure(cls, localSensorsFile:str=None):
        """
        Configures the server to use that folder.
        :param folder: The storage folder.
        :type folder: str
        """
        folder = os.environ.get('DATA_FOLDER', None)
        if folder is None:
            print(f"Error: The required environment variable DATA_FOLDER is not set.")
            sys.exit(1)
        port = None
        portValue = os.environ.get('UDP_PORT', None)
        if portValue:
            port = int(portValue)

        cls._instance = Server(folder, port, localSensorsFile)
        cls.configure_logging()

    @classmethod
    def configure_logging(cls):
        """
        Configures the logging system.
        """
        level = logging.INFO
        default_logger = logging.getLogger()
        formatter = None
        for handler in logging.getLogger("gunicorn").handlers:
            formatter = handler.getFormatter()
            break;
        if formatter is None:
            formatter = logging.Formatter(
                '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S %z')

        handlers_to_remove = []
        for handler in default_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handlers_to_remove.append(handler)
        for handler in handlers_to_remove:
            default_logger.removeHandler(handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        default_logger.setLevel(level)
        default_logger.addHandler(console_handler)
        for handler in default_logger.handlers:
            handler.setFormatter(formatter)
        default_level = default_logger.getEffectiveLevel()

        a2sensor_logger = logging.getLogger("a2sensor")
        a2sensor_logger.setLevel(level)
        for handler in a2sensor_logger.handlers:
            handler.setFormatter(formatter)

    @classmethod
    def instance(cls):
        """
        Retrieves the singleton instance.
        :return: Such instance.
        :rtype: a2sensor.sensor_collect.Server
        """
        return cls._instance
