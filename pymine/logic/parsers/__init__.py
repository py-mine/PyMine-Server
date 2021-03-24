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
            
import classyjson
import importlib
import os

from pymine.types.abc import AbstractParser

parsers = classyjson.ClassyDict()

for root, dirs, files in os.walk(os.path.join("pymine", "logic", "parsers")):
    for file in filter((lambda f: f.endswith(".py") and "__" not in f), files):
        module = importlib.import_module(os.path.join(root, file)[:-3].replace("\\", "/").replace("/", "."))

        for name, obj in module.__dict__.items():
            try:
                if issubclass(obj, AbstractParser):
                    parsers[name] = obj
            except (TypeError, KeyError):  # can't call issubclass() on non-classes
                pass
