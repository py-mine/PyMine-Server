"""Contains base packets."""

from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet


__all__ = ('PacketClientboundJSON',)


class PacketClientboundJSON(Packet):
    """Base class used in most client-bound play packets."""

    def encode(self):
        return Buffer.pack_json(self.response_data)
