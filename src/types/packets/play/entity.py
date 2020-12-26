"""Contains packets related to entities."""

from __future__ import annotations
import nbt

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayBlockEntityData',)


class PlayBlockEntityData(Packet):
    """Sets the block entity associated with the block at the given location. (Server -> Client).


    :param int x: The x coordinate of the position.
    :param int y: The y coordinate of the position.
    :param int z: The z coordinate of the position.
    :param int action: The action to be carried out (see https://wiki.vg/Protocol#Block_Entity_Data).
    :param nbt.TAG nbt_data: The nbt data associated with the action/block.
    :attr type id_: Unique packet ID.
    :attr x:
    :attr y:
    :attr z:
    :attr action:
    :attr nbt_data:
    """

    id_ = 0x09
    to = 1

    def __init__(self, x: int, y: int, z: int, action: int, nbt_data: nbt.TAG) -> None:
        super().__init__()

        self.x = x
        self.y = y
        self.z = z
        self.action = action
        self.nbt_data = nbt_data

    def encode(self) -> bytes:
        return Buffer.pack_pos(self.x, self.y, self.z) + \
            Buffer.pack('B', self.action) + Buffer.pack_nbt(self.nbt_data)
