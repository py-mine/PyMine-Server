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

"""Contains LoginSetCompression which is technically part of the login process."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("LoginSetCompression",)


class LoginSetCompression(Packet):
    """While not directly related to logging in, this packet is sent by the server during the login process. (Server -> Client)

    :param int comp_thresh: Compression level of future packets, -1 to disable compression.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar comp_thresh:
    """

    id = 0x03
    to = 1

    def __init__(self, comp_thresh: int = -1) -> None:
        super().__init__()

        self.comp_thresh = comp_thresh

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.comp_thresh)
