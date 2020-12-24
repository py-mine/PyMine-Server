"""Contains statistic packet"""

from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet


__all__ = ('PlayStatistics',)


class PlayStatistics(Packet):
    """Sent as a response to Client Status 0x04 (id 1). Will only send the changed values if previously requested. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x06)

    def encode(self):
        return Buffer.pack_json(self.response_data)
