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
"""Contains packets related to commands"""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayDeclareCommands",)


class PlayDeclareCommands(Packet):
    """Tells the clients what commands there are.

    :param list nodes: The command nodes.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr nodes:
    """

    id = 0x10
    to = 1

    def __init__(self, nodes: list) -> None:  # nodes is a list of dicts, assumes first node is the root node
        super().__init__()

        self.nodes = nodes

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(len(self.nodes))
            + b"".join([Buffer.pack_node(node) for node in self.nodes])
            + Buffer.pack_varint(0)
        )
