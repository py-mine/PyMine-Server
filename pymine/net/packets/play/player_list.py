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

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.chat import Chat

__all__ = ("PlayPlayerListHeaderAndFooter",)


class PlayPlayerListHeaderAndFooter(Packet):
    """yep"""

    id = 0x53
    to = 1

    def __init__(self, header: Chat, footer: Chat) -> None:
        super().__init__()

        self.header = header
        self.footer = footer

    def encode(self) -> bytes:
        return Buffer.pack_chat(self.header) + Buffer.pack_chat(self.footer)
