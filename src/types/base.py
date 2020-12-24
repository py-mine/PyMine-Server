"""Contains base packets."""

from src.types.buffer import Buffer
from src.types.packet import Packet


__all__ = ('PacketClientboundJSON',)


class PacketClientboundJSON(Packet):
    """Base class used in most client-bound play packets."""

    def __init__(self, id: int):
        super.__init__(id)

    def encode(self):
        return Buffer.pack_json(self.response_data)  # assumes response_data is present
