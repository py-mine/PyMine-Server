"""Contains statistic packet."""

from __future__ import annotations

from src.types.base import PacketClientboundJSON


__all__ = ('PlayStatistics',)


class PlayStatistics(PacketClientboundJSON):
    """Sent as a response to Client Status 0x04 (id 1). Will only send the changed values if previously requested. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x06)
