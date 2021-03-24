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


def make_immutable(obj: object) -> object:
    """Recursively converts lists to tuples and dictionaries to maps.

    :param object obj: A list or dict object.
    :return: Should be an immutable list or dict, or whatever else put in.
    :rtype: object
    """

    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = make_immutable(v)

        return Map(obj)

    if isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = make_immutable(v)

        return tuple(obj)

    return obj
