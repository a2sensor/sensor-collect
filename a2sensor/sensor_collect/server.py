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
from flask import Flask, request, jsonify

class Server():
    """
    Represents a Server that collects data from sensors.

    Class name: Server

    Responsibilities:
        - Collect data from sensors.

    Collaborators:
        - None
    """
    def __init__(self):
        """
        Creates a new Server instance.
        """
        super().__init__()
        self._app = Flask(__name__)
        self.setup_routes()

    @property
    def app(self):
        """
        Retrieves the Flask application.
        :return: Such instance.
        :rtype: flask.Flask
        """
        return self._app

    def setup_routes(self):
        """
        Defines the application routes.
        """
        self.app.add_url_rule('/v1/<sensorId>/measure', 'measure_endpoint', self.measure_endpoint, methods=['PUT'])

    def measure_endpoint(self, sensorId):
        """
        Collects a new measure from given sensor.
        :param sensorId: The id of the sensor.
        :type sensorId: str
        """
        if not request.is_json:
            return jsonify({"error": "Invalid JSON format"}), 400

        data = request.get_json()
        value1 = data.get("value1")
        value2 = data.get("value2")
        value3 = data.get("value3")
        value4 = data.get("value4")

        # Process or store the data (for now, just print)
        print(f"Sensor ID: {sensorId}")
        print(f"Value 1: {value1}")
        print(f"Value 2: {value2}")
        print(f"Value 3: {value3}")
        print(f"Value 4: {value4}")

        return jsonify({"status": "success"}), 200

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    server = Server()
    server.run()
