"""Contains spawn packets."""

from __future__ import annotations
from src.types.packet import Packet

__all__ = (
    'PlayEntitySpawn',
    'PlayLivingEntitySpawn',
    'PlayPaintingSpawn',
    'PlaySpawnExperienceOrb',
)


class PlayEntitySpawn(Packet):
    """Sent by the server when a vehicle or other non-living entity is created. Client bound(Client -> Server)."""

    id_ = 0x00

    def __init__(self, response_data: dict) -> None:
        super().__init__()


class PlayLivingEntitySpawn(Packet):
    """Sent by the server when a living entity is spawned.  Client bound(Client -> Server)."""

    id_ = 0x02

    def __init__(self, response_data: dict) -> None:
        super().__init__()


class PlayPaintingSpawn(Packet):
    """This packet shows location, name, and type of painting.  Client bound(Client -> Server)."""

    id_ = 0x03

    def __init__(self, response_data: dict) -> None:
        super().__init__()


class PlaySpawnExperienceOrb(Packet):
    """Spawns one or more experience orbs. Client bound(Client -> Server)."""

    id_ = 0x01

    def __init__(self, response_data: dict) -> None:
        super().__init__()
