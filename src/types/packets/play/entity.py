from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet
"""Contains packets concerning entitys"""

__all__ = ('PlayEntitySpawn',)


class PlayEntitySpawn(Packet):
    """Sent by the server when a vehicle or other non-living entity is created. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x00)

    def encode(self):
        return Buffer.pack_json(self.response_data)


class PlayLivingEntitySpawn(Packet):
    """Sent by the server when a living entity is spawned.  Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x02)

    def encode(self):
        return Buffer.pack_json(self.response_data)
