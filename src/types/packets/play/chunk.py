from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayUnloadChunk',)

class PlayUnloadChunk(Packet):
    """Tells the client to unload a chunk column. Clientbound(Server => Client)"""
    id = 0x1C
    to = 1

    def __init__(self, chunk_x: int, chunk_z: int):
        self.chunk_x, self.chunk_z = chunk_x, chunk_z
    def encode(self):
        return Buffer.pack('i', self.chunk_x) + Buffer.pack('i', self.chunk_z)
