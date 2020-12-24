"""Contains statistic packet."""

from __future__ import annotations

from src.types.packet import PacketClientboundJSON

__all__ = ('PlayStatistics',)


class PlayStatistics(PacketClientboundJSON):
    """Sent as a response to Client Status 0x04 (id 1). Will only send the changed values if previously requested. Client bound(Client -> Server)."""

    id_ = 0x06

    def __init__(self, response_data: dict) -> None:
        super().__init__()
