"""
a2sensor/sensor_collect/local_sensors.py

This script defines the LocalSensors class.

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
from collections import deque
import logging
import RPi.GPIO as GPIO
import threading
import time
import toml
from typing import Dict, List

class LocalSensors():
    """
    Represents the local sensors attached.

    Class name: LocalSensors

    Responsibilities:
        - Collect data from sensors.

    Collaborators:
        - None
    """
    _instance = None

    def __init__(self, configFile:str, callback):
        """
        Creates a new LocalSensors instance.
        :param configFile: The configuration file.
        :type configFile: str
        :param callback: The callback function to call for each read of a sensor.
        :type callbalk: function
        """
        super().__init__()
        self._config_file = configFile
        self._sensors = {}
        self._callback = callback
        self._previous_measures = {}
        self._exit_event = threading.Event()
        self.configure()

    @property
    def config_file(self) -> str:
        """
        Retrieves the location of the configuration file.
        :return: Such path.
        :rtype: str
        """
        return self._config_file

    @property
    def sensors(self) -> Dict[str, Dict]:
        """
        Retrieves the information about the sensors.
        :return: Such information.
        :rtype: Dict[str, Dict]
        """
        return self._sensors

    @property
    def callback(self):
        """
        Retrieves the callback function to call for each read of a sensor.
        :return: Such callback function.
        :rtype: function
        """
        return self._callback

    @property
    def previous_measures(self) -> Dict[str, List[bool]]:
        """
        Retrieves a dictionary with the previous measures of each sensor.
        :return: Such dictionary.
        :rtype: Dict[str, List[bool]]
        """
        return self._previous_measures

    @property
    def exit_event(self):
        """
        Retrieves the exit event.
        :return: Such event.
        :rtype: threading.Event
        """
        return self._exit_event

    def configure(self):
        """
        Reads the settings from the configuration file.
        """
        config = toml.load(self.config_file)

        for sensor, attributes in config.items():
            self.sensors[sensor] = attributes
            self.previous_measures[sensor] = deque(maxlen=attributes.get('stuck_threshold', 10))

    def start(self):
        """
        Starts reading from the attached sensors.
        """
        # Create and start a thread for each sensor
        threads = []
        for sensor in self.sensors:
            thread = threading.Thread(target=self.read_sensor, args=(sensor, self.sensors[sensor]['pin'],))
            threads.append(thread)
            thread.start()

        # Keep the script running
        try:
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            logging.getLogger("a2sensor").warn("Exiting")
            self.exit_event.set()
            for thread in threads:
                thread.join()
        finally:
            GPIO.cleanup()

    def read_sensor(self, sensorKey:str, pin:int):
        """
        Reads from a sensor.
        :param sensorKey: The key of the sensor.
        :type sensorKey: str
        :param pin: The pin of the sensor.
        :type pin: int
        """
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.IN)
            while not self.exit_event.is_set():
                value = GPIO.input(pin)
                previous_values = self.previous_measures[sensorKey]
                previous_values.append(value)
                self.callback(self.sensors[sensorKey].get('id', sensorKey), self.sensors[sensorKey].get('name', sensorKey), self.to_status(previous_values))
                time.sleep(self.sensors[sensorKey].get('wait', 1))
        except KeyboardInterrupt:
            logging.getLogger("a2sensor").warn("Exiting")
            self.exit_event.set()

    def to_status(self, previousValues: List[bool]) -> str:
        """
        Converts given values from the sensors into a sensor status.
        :param previousValues: The previous values.
        :type previousValues: List[bool]
        :return: The status.
        :rtype: str
        """
        if all(previousValues):
            result = "stuck"
        elif all(not x for x in previousValues):
            result = "empty"
        else:
            result = "ok"

        return result
