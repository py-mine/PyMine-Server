"""Contains packets concerning light."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayUpdateLight',)


class PlayUpdateLight(Packet):
    """Updates light levels for a chunk."""

    id = 0x23
    to = 1

    def __init__(
            self,
            chunk_x: int,
            chunk_z: int,
            trust_edges: bool,
            sky_light_mask: int,
            block_light_mask: int,
            empty_sky_light_mask: int,
            empty_block_light_mask: int,
            sky_light_array: list,
            block_light_array: list) -> None:
        super().__init__()
        
        self.chunk_x, self.chunk_z = chunk_x, chunk_z
        self.trust_edges = trust_edges
        self.sky_light_mask, self.empty_sky_light_mask = sky_light_mask, empty_sky_light_mask
        self.block_light_mask, self.empty_block_light_mask = block_light_mask, empty_block_light_mask
        self.sky_light_array = sky_light_array
        self.block_light_array = block_light_array

    def encode(self) -> bytes:
        return Buffer.pack('i', self.chunk_x) + Buffer.pack('i', self.chunk_z) + Buffer.pack('?', self.trust_edges) + \
            Buffer.pack_varint(self.sky_lm) + Buffer.pack_varint(self.block_lm) + Buffer.pack_varint(self.esky_lm) + \
            Buffer.pack_varint(self.eblock_lm) + Buffer.pack_array('c', self.sky_light_array) + \
            Buffer.pack_array('c', self.block_light_array)
