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
import os
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

    def __init__(self, storageFolder:str):
        """
        Creates a new Server instance.
        :param storageFolder: The folder to store measures.
        :type storageFolder: str
        """
        super().__init__()
        self._storage_folder = storageFolder

        if not os.path.exists(self._storage_folder):
            os.makedirs(self._storage_folder)  # create the folder if it doesn't exist

    @property
    def storage_folder(self):
        """
        Retrieves the storage folder.
        :return: Such value.
        :rtype: str
        """
        return self._storage_folder

    def save_to_file(self, sensorId:str, data:Dict):
        """
        Saves given measure to disk.
        :param sensorId: The id of the sensor.
        :type sensorId: str
        :param data: The measure.
        :type data: Dict
        """
        folder = os.path.join(self.storage_folder, sensorId)
        if not os.path.exists(folder):
            os.makedirs(folder)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        filepath = os.path.join(folder, f"{timestamp}.json")

        with open(filepath, 'w') as file:
            json.dump(data, file)

    @classmethod
    def configure(cls, folder:str):
        """
        Configures the server to use that folder.
        :param folder: The storage folder.
        :type folder: str
        """
        cls._instance = Server(folder)

    @classmethod
    def instance(cls):
        """
        Retrieves the singleton instance.
        :return: Such instance.
        :rtype: a2sensor.sensor_collect.Server
        """
        return cls._instance

def parse_cli():
    """
    Parses the command-line arguments.
    :return: The Server instance.
    :rtype: a2sensor.sensor_collect.Server
    """
    parser = argparse.ArgumentParser(description="Runs A2Sensor Sensor-Collect")
    parser.add_argument('-d', '--data-folder', required=True, help='The data folder')
    args, unknown_args = parser.parse_known_args()
    Server.configure(args.data_folder)

app = Flask(__name__)

@app.route("/v1/<sensorId>/measure", methods=['PUT'])
def measure_endpoint(sensorId: str):
    """
    Collects a new measure from given sensor.
    :param sensorId: The id of the sensor.
    :type sensorId: str
    """
    if not request.is_json:
        return jsonify({"error": "Invalid JSON format"}), 400

    data = request.get_json()

    Server.instance().save_to_file(sensorId, data)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    Server.parse_cli()
    app.run()
