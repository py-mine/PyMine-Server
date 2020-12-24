"""Contains packets related to bosses."""

from __future__ import annotations

from src.types.packet import Packet

__all__ = ('PlayBossBar',)


class PlayBossBar(Packet):
    """Has boss bar stuff in it. Client bound(Client -> Server)."""

    id_ = 0x0C

    def __init__(self, response_data: dict) -> None:
        super().__init__()
