"""Contains spawn packets."""

from __future__ import annotations
from src.types.packet import PacketClientboundJSON


__all__ = ('PlayEntitySpawn', 'PlayLivingEntitySpawn',
           'PlayPaintingSpawn', 'PlaySpawnExperienceOrb')


class PlayEntitySpawn(PacketClientboundJSON):
    """Sent by the server when a vehicle or other non-living entity is created. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super().__init__(0x00)


class PlayLivingEntitySpawn(PacketClientboundJSON):
    """Sent by the server when a living entity is spawned.  Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super().__init__(0x02)


class PlayPaintingSpawn(PacketClientboundJSON):
    """This packet shows location, name, and type of painting.  Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super().__init__(0x03)


class PlaySpawnExperienceOrb(PacketClientboundJSON):
    """Spawns one or more experience orbs. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super().__init__(0x01)
