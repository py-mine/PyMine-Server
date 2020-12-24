"""Contains animation packets"""

from __future__ import annotations

from src.types.base import PacketClientboundJSON
from src.types.buffer import Buffer
from src.types.packet import Packet


__all__ = ('PlayEntityAnimation',)


class PlayEntityAnimation(PacketClientboundJSON):
    """Sent whenever an entity should change animation. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x05)
