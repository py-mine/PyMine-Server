"""Contains packets related to entities."""

from __future__ import annotations
import nbt

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = (
    'PlayBlockEntityData',
    'PlayQueryEntityNBT',
    'PlayInteractEntity'
)


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
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
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


class PlayInteractEntity(Packet):
    """Sent when a client clicks another entity, see here: https://wiki.vg/Protocol#Interact_Entity. (Client -> Server)

    :param int entity_id: The ID of the entity interacted with.
    :param int type_: Either interact (0), attack (1), or interact at (2).
    :param int target_x: The x coordinate of where the target is, can be None.
    :param int target_y: The y coordinate of where the target is, can be None.
    :param int target_z: The z coordinate of where the target is, can be None.
    :param int hand: The hand used.
    :param bool sneaking: Whether the client was sneaking or not.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr entity_id:
    :attr type_:
    :attr target_x:
    :attr target_y:
    :attr target_z:
    :attr hand:
    :attr sneaking:
    """

    id = 0x0E
    to = 0

    def __init__(
            self,
            entity_id: int,
            type_: int,
            target_x: int,
            target_y: int,
            target_z: int,
            hand: int,
            sneaking: bool) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.type_ = type_
        self.target_x = target_x
        self.target_y = target_y
        self.target_z = target_z
        self.hand = hand
        self.sneaking = sneaking

    @classmethod
    def decode(cls, buf: Buffer) -> PlayInteractEntity:
        entity_id = buf.unpack_varint()
        type_ = buf.unpack_varint()

        target_x, target_y, target_z = None

        if buf.unpack_bool():
            target_x = buf.unpack_varint()

        if buf.unpack_bool():
            target_y = buf.unpack_varint()

        if buf.unpack_bool():
            target_z = buf.unpack_varint()

        if buf.unpack_bool():
            hand = buf.unpack_varint()

        sneaking = buf.unpack_bool()

        return cls(entity_id, type_, target_x, target_y, target_z, hand, sneaking)


class PlayEntityAction(Packet):
    """Sent by the client to indicate it has performed a certain action. (Client -> Server)

    :param int entity_id: The ID of the entity.
    :param int action_id: The action occurring, see here: https://wiki.vg/Protocol#Entity_Action.
    :param int jump_boost: Used with jumping while riding a horse.
    :attr type id: Description of parameter `id`.
    :attr type to: Description of parameter `to`.
    :attr entity_id:
    :attr action_id:
    :attr jump_boost:
    """

    id = 0x1C
    to = 0

    def __init__(self, entity_id: int, action_id: int, jump_boost: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.action_id = action_id
        self.jump_boost = jump_boost

    @classmethod
    def decode(cls, buf: Buffer) -> PlayEntityAction:
        return cls(buf.unpack_varint(), buf.unpack_varint(), buf.unpack_varint())
