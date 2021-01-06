"""Contains packets concerning light."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.bufffer import Buffer


class PlayUpdateLight(Packer):
    """Updates light levels for a chunk."""

    id = 0x23
    to = 1

    def __init__(self, chunk_x: int, chunk_z: int, trust_edges: bool, sky_light_mask: int, block_light_mask: int, empty_sky_light_mask: int, empty_block_light_mask: int, sky_light_arr: list, block_light_Arr: list):  # nopep8
    super().__init__()
    self.chunk_x, , self.chunk_z = chunk_x, chunk_z
    self.trust_edges = trust_edges
    self.sky_lm, self.block_lm, self.esky_lm, self.eblock_lm = sky_light_mask, block_light_mask, empty_sky_light_mask, empty_block_light_mask
    self.sklr, self.blkr = sky_light_array, block_light_array
