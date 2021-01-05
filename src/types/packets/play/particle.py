"""Contains packets that are related to particles."""
from __future__ import annotations

from src.types.packets import Packet
from src.types.buffer import Buffer


class PlayParticle(Packet):
    """Displays the named particle."""

    id = 0x22
    to = 1

    def __init__(self, particle_id: int, long_distance: bool, x: int, y: int, z: int, offset_x: float, offset_y: float, offset_z: float, particle_data: float, particle_count: int, data: dict):

        super().__init__()
        self.part_id = particle_id
        self.long_dist = long_distance
        self.x, self.y, self.z = x, y, z
        self.off_x, self.off_y, self.set_z = offset_x, offset_y, offset_z
        self.part_data, self.part_count, self.data = particle_data, particle_count, data

    def encode(self):
        return Buffer.pack('i', self.part_id) + Buffer.pack('?', self.long_dist) + Buffer.pack('d', self.x) +\
            Buffer.pack('d', self.y) + Buffer.pack('d', self.z) + Buffer.pack('d', self.off_x) +\
            Buffer.pack('d', self.off_y) + Buffer.pack('d', self.off_z) + Buffer.pack('f', self.part_data) +\
            Buffer.pack('i', self.part_count) + Buffer.pack_particle(self.data)
