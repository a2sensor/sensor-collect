"""
a2sensor/sensor_collect/flask_app.py

This script defines the Flask app.

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
import os

app = Flask(__name__)

@app.route("/v1/<sensorId>/measure", methods=["PUT"])
def measure_endpoint(sensorId: str):
    """
    Collects a new measure from given sensor.
    :param sensorId: The id of the sensor.
    :type sensorId: str
    """
    if not request.is_json:
        return jsonify({"error": "Invalid JSON format"}), 400

    data = request.get_json()

    from .server import Server
    result = {}
    sensorName = data.get('sensorName', None)
    sensorStatus = data.get('sensorStatus', None)
    if sensorName is None or sensorStatus is None or sensorStatus not in [ "empty", "ok", "stuck" ]:
        status_code = 400
        result["status"] = "invalid request"
        messages = []
        if sensorName is None:
            messages.append("Missing 'sensorName' attribute")
        if sensorStatus is None:
            messages.append("Missing 'sensorStatus' attribute")
        elif sensorStatus not in [ "empty", "ok", "stuck" ]:
            messages.append(f"Provided 'sensorStatus' is {sensorStatus} and must be one of 'empty', 'ok' or 'stuck'")
        result["messages"] = messages

    else:
        status_code = 200
        result["status"] = "success"
        Server.instance().save_to_file(sensorId, sensorName, sensorStatus)

    return jsonify(result), status_code

if Server.instance() is None:
    folder = os.environ.get('DATA_FOLDER', None)
    if folder is None:
        print(f"Error: The required environment variable DATA_FOLDER is not set.")
        sys.exit(1)
    file = os.environ.get('LOCAL_SENSORS_CONFIG_FILE', None)
    if file is None:
        print(f"Error: The required environment variable LOCAL_SENSORS_CONFIG_FILE is not set.")
        sys.exit(1)
    Server.configure(folder, file)
