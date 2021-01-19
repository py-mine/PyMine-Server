"""Contains packets related to the world and world border"""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ()


class PlayWorldBorder(Packet):
    """Changes settings for the world border. (Server -> Client)

    :param int action: One of set size (0), lerp size (1), set center (2), init (3), set warning time (4), or set warning blocks (5)
    :param dict data: Depends upon the action, see here: https://wiki.vg/Protocol#World_Border.
    :attr type id: Unique packet ID.
    :attr type to: Packet direction.
    :attr action:
    :attr data:
    """

    id = 0x3D
    to = 1

    def __init__(self, action: int, data: dict) -> None:
        super().__init__()

        self.action = action
        self.data = data

    def encode(self) -> bytes:
        out = Buffer.pack_varint(self.action)

        if self.action == 0:  # set size
            out += Buffer.pack('d', self.data['diameter'])
        elif self.action == 1:  # lerp size
            out += Buffer.pack('d', self.data['old_diameter']) + Buffer.pack('d', self.data['new_diameter']) + \
                Buffer.pack_varint(self.data['speed'])
        elif self.action == 2:  # set center
            out += Buffer.pack('d', self.data['x']) + Buffer.pack('d', self.data['z'])
        elif self.action == 3:  # initialize
            out += Buffer.pack('d', self.data['x']) + Buffer.pack('d', self.data['z']) + \
                Buffer.pack('d', self.data['old_diameter']) + Buffer.pack('d', self.data['new_diameter']) + \
                Buffer.pack_varint(self.data['speed']) + Buffer.pack_varint(self.data['portal_teleport_boundary']) + \
                Buffer.pack_varint(self.data['warning_blocks']) + Buffer.pack_varint(self.data['warning_time'])
        elif self.action == 4:  # set warning time
            out += Buffer.pack_varint(self.data['warning_time'])
        elif self.action == 5:  # set warning blocks
            out += Buffer.pack_varint(self.data['warning_blocks'])

        return out
