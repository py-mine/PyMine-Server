"""Contains packets related to entitys."""

from __future__ import annotations

from src.types.packet import PacketClientboundJSON


__all__ = ('PlayBlockEntityData',)


class PlayBlockEntityData(PacketClientboundJSON):
    """Sets the block entity associated with the block at the given location. Clientbound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super().__init__(0x09)
