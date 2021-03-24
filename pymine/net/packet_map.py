# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import importlib
import os

from pymine.util.immutable import make_immutable
from pymine.data.states import STATES

__all__ = (
    "PACKET_MAP",
    "PACKET_MAP_CLIENTBOUND",
)


def load_packets():
    packet_path = os.path.join("pymine", "net", "packets")
    packet_dot_path = packet_path.replace("\\", "/").replace("/", ".")

    packet_map = {}
    packet_map_clientbound = {}

    for state_name in os.listdir(packet_path):
        state = STATES.encode(state_name)

        packet_map[state] = {}
        packet_map_clientbound[state] = {}

        for file in filter((lambda f: f.endswith(".py")), os.listdir(os.path.join(packet_path, state_name))):
            module = importlib.import_module(f"{packet_dot_path}.{state_name}.{file[:-3]}")

            for name in module.__all__:
                packet = module.__dict__.get(name)
                if packet.to == 2:
                    packet_map[state][packet.id] = packet_map_clientbound[state][packet.id] = packet
                elif packet.to == 1:
                    packet_map_clientbound[state][packet.id] = packet
                elif packet.to == 0:
                    packet_map[state][packet.id] = packet
                else:
                    raise ValueError(f"The direction of packet {type(packet).__name__} is invalid.")

    return make_immutable(packet_map), make_immutable(packet_map_clientbound)


PACKET_MAP, PACKET_MAP_CLIENTBOUND = load_packets()
