"""Contains packets related to game state."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ('PlayChangeGameState',)


class PlayChangeGameState(Packet):
    """insert fancy doscstring here (server -> client)"""

    id = 0x1D
    to = 1

    def __init__(self, reason: int, value: float) -> None:
        super().__init__()

        self.reason = reason
        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack('B', self.reason) + Buffer.pack('f', self.value)
