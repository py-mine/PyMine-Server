"""Contains packets related to entitys."""

from __future__ import annotations

from src.types.packet import Packet

__all__ = ('PlayBlockEntityData',)


class PlayBlockEntityData(Packet):
    """Sets the block entity associated with the block at the given location. Clientbound(Client -> Server)."""

    id_ = 0x09

    def __init__(self, response_data: dict) -> None:
        super().__init__()
