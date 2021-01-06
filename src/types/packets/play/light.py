"""Contains packets concerning light."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.bufffer import Buffer


class PlayUpdateLight(Packet):
    """Updates light levels for a chunk."""

    id = 0x23
    to = 1

    def __init__(self, chunk_x: int, chunk_z: int, trust_edges: bool, sky_light_mask: int, block_light_mask: int, empty_sky_light_mask: int, empty_block_light_mask: int, sky_light_arr: list, block_light_arr: list):  # nopep8
        super().__init__()
        self.chunk_x, , self.chunk_z = chunk_x, chunk_z
        self.trust_edges = trust_edges
        self.sky_lm, self.block_lm, self.esky_lm, self.eblock_lm = sky_light_mask, block_light_mask, empty_sky_light_mask, empty_block_light_mask
        self.sklr, self.blkr = sky_light_array, block_light_array

    def encode(self):
        return Buffer.pack('i', self.chunk_x) + Buffer.pack('i', self.chunk_z) + Buffer.pack('?', self.trust_edges) +\
            Buffer.pack_varint(self.sky_lm) + Buffer.pack_varint(self.block_lm) + Buffer.pack_varint(self.esky_lm) +\
            Buffer.pack_varint(self.eblock_lm) + Buffer.pack_array('c', self.sklr) + Buffer.pack_array('c', self.blkr)
