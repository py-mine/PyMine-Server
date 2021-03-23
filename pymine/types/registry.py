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
from immutables import Map

from pymine.util.immutable import make_immutable


class Registry:
    def __init__(self, data: object, data_reversed: object = None) -> None:
        self.data_reversed = data_reversed

        if isinstance(data, (dict, Map)):
            self.data = make_immutable(data)

            if data_reversed is None:
                self.data_reversed = make_immutable({v: k for k, v in data.items()})
        elif isinstance(data, (list, tuple)):
            self.data_reversed = data
            self.data = make_immutable({v: i for i, v in enumerate(self.data_reversed)})
        else:
            raise TypeError("Creating a registry from something other than a dict, Map, tuple, or list isn't supported")

    def encode(self, key: object) -> object:  # most likely an identifier to an int
        return self.data[key]

    def decode(self, value: object) -> object:  # most likely a numeric id to a string identifier
        return self.data_reversed[value]
