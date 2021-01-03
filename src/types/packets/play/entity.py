"""Contains packets related to entities."""

from __future__ import annotations
import nbt

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayBlockEntityData', 'PlayQueryEntityNBT',)


class PlayBlockEntityData(Packet):
    """Sets the block entity associated with the block at the given location. (Server -> Client).

    :param int x: The x coordinate of the position.
    :param int y: The y coordinate of the position.
    :param int z: The z coordinate of the position.
    :param int action: The action to be carried out (see https://wiki.vg/Protocol#Block_Entity_Data).
    :param nbt.TAG nbt_data: The nbt data associated with the action/block.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr y:
    :attr z:
    :attr action:
    :attr nbt_data:
    """

    id = 0x09
    to = 1

    def __init__(self, x: int, y: int, z: int, action: int, nbt_data: nbt.TAG) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.action = action
        self.nbt_data = nbt_data

    def encode(self) -> bytes:
        return Buffer.pack_pos(self.x, self.y, self.z) + Buffer.pack('B', self.action) + \
            Buffer.pack_nbt(self.nbt_data)


class PlayQueryEntityNBT(Packet):
    """Sent by the client when Shift+F3+I is used. (Client -> Server)

    :param int transaction_id: Incremental ID used so the client can verify responses.
    :param int entity_id: The ID of the entity to query.
    :attr type id: Unique packet ID.
    :attr type to: Packet direction.
    :attr transaction_id:
    :attr entity_id:
    """

    id = 0x0D
    to = 0

    def __init__(self, transaction_id: int, entity_id: int) -> None:
        super().__init__()

        self.transaction_id = transaction_id
        self.entity_id = entity_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlayQueryEntityNBT:
        return cls(buf.unpack_varint(), buf.unpack_varint())
