from __future__ import annotations

from src.types.base import PacketClientboundJSON
from src.types.buffer import Buffer
from src.types.packet import Packet
"""Contains spawn packets"""

__all__ = ('PlayEntitySpawn', 'PlayLivingEntitySpawn',
           'PlayPaintingSpawn', 'PlaySpawnExperienceOrb')


class PlayEntitySpawn(PacketClientboundJSON):
    """Sent by the server when a vehicle or other non-living entity is created. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x00)


class PlayLivingEntitySpawn(Packet):
    """Sent by the server when a living entity is spawned.  Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x02)

    def encode(self):
        return Buffer.pack_json(self.response_data)


class PlayPaintingSpawn(Packet):
    """This packet shows location, name, and type of painting.  Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x03)

    def encode(self):
        return Buffer.pack_json(self.response_data)


class PlaySpawnExperienceOrb(Packet):
    """Spawns one or more experience orbs. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x01)

    def encode(self):
        return Buffer.pack_json(self.response_data)
