"""
a2sensor/sensor_collect/udp_server.py

This script defines an UDP server.

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
import logging
import socket

def udp_server():
    """
    Creates an UDP server.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        logging.getLogger("a2sensor").info(
            f"UDP server running at port {Server.instance().udp_port}"
        )
        # Bind the socket to a specific address and port
        from .server import Server

        s.bind(("0.0.0.0", Server.instance().udp_port))

        while True:
            # Receive data from the client
            data, address = s.recvfrom(1024)
            print(f"Received data: {data.decode()} from {address}")

            # Optionally, send a response
            s.sendto(b"ACK", address)
