"""Contains packets related to players."""

from __future__ import annotations

from src.types.base import PacketClientboundJSON


__all__ = ('PlayAcknowledgePlayerDigging',)


class PlayAcknowledgePlayerDigging(PacketClientboundJSON):
    """Acknowledges player digging. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x05)
