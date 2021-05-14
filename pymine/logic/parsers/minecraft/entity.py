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

import random
import uuid

from pymine.types.abc import AbstractParser
from pymine.api.errors import ParsingError
from pymine.util.misc import DualMethod


class UUID(AbstractParser):
    @DualMethod
    def parse(self, s: str) -> tuple:
        section = s.split()[0]

        try:
            return len(section), uuid.UUID(section)
        except ValueError:
            raise ParsingError("invalid value for a UUID provided.")
