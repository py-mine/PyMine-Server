"""Contains packets related to players."""

from __future__ import annotations

from src.types.packet import Packet

__all__ = ('PlayAcknowledgePlayerDigging',)


class PlayAcknowledgePlayerDigging(Packet):
    """Acknowledges player digging. Client bound(Client -> Server)."""

    id_ = 0x07

    def __init__(self, response_data: dict) -> None:
        super().__init__()
