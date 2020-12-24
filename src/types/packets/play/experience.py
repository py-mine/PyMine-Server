from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet
"""Contains packets concerning experience"""

__all__ = ('PlaySpawnExperienceOrb',)


class PlaySpawnExperienceOrb(Packet):
    """Spawns one or more experience orbs. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x01)

    def encode(self):
        return Buffer.pack_json(self.response_data)
