from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet
"""Contains animation packets"""

__all__ = ('PlayEntityAnimation',)


class PlayEntityAnimation(Packet):
    """Sent whenever an entity should change animation. sClient bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x05)

    def encode(self):
        return Buffer.pack_json(self.response_data)
