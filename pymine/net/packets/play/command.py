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

    def __init__(self, nodes: list) -> None:  # nodes is a list of dicts
        super().__init__()

        self.nodes = nodes

    def encode(self) -> bytes:
        out = Buffer.pack_varint(len(self.nodes))

        for node in self.nodes:
            out += Buffer.pack("b", node["flags"]) + Buffer.pack

        return out + Buffer.pack_varint(0)
