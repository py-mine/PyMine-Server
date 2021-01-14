"""Contains packets related to blocks."""

from __future__ import annotations
from nbt import nbt

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    'PlayBlockAction',
    'PlayBlockChange',
    'PlayQueryBlockNBT',
    'PlayBlockPlacement',
    'PlayNBTQueryResponse',
)


class PlayBlockAction(Packet):
    """This packet is used for a number of actions and animations performed by blocks. (Server -> Client)

    :param int x: The x coordinate of the location where this occurs.
    :param int y: The y coordinate of the location where this occurs.
    :param int z: The z coordinate of the location where this occurs.
    :param int action_id: Block action ID, see here: https://wiki.vg/Block_Actions.
    :param int action_param: Action param of the action, see here: https://wiki.vg/Block_Actions.
    :param int block_type: The type of block which the action is for.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr y:
    :attr z:
    :attr action_id:
    :attr action_param:
    :attr block_type:
    """

    id = 0x0A
    to = 1

    def __init__(self, x: int, y: int, z: int, action_id: int, action_param: int, block_type: int) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.action_id = action_id
        self.action_param = action_param
        self.block_type = block_type

    def encode(self) -> bytes:
        return Buffer.pack_pos(self.x, self.y, self.z) + Buffer.pack('B', self.action_id) + \
            Buffer.pack('B', self.action_param) + Buffer.pack_varint(self.block_type)


class PlayBlockChange(Packet):
    """Fired when a block is changed within the render distance. (Server -> Client)

    :param int x: The x coordinate of the location where this occurs.
    :param int y: The y coordinate of the location where this occurs.
    :param int z: The z coordinate of the location where this occurs.
    :param int block_id: Block ID of what to change the block to.
    :attr int id: Unique packet ID.
    :attr x:
    :attr y:
    :attr z:
    :attr block_id:
    """

    id = 0x0B
    to = 1

    def __init__(self, x: int, y: int, z: int, block_id: int) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.block_id = block_id

    def encode(self) -> bytes:
        return Buffer.pack_pos(self.x, self.y, self.z) + Buffer.pack_varint(self.block_id)


class PlayQueryBlockNBT(Packet):
    """Used when SHIFT+F3+I is used on a block. (Client -> Server)

    :param int transaction_id: Number used to verify that a response matches.
    :param int x: The x coordinate of the block.
    :param int y: The y coordinate of the block.
    :param int z: The z coordinate of the block.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr transaction_id:
    :attr x:
    :attr y:
    :attr z:
    """

    id = 0x01
    to = 0

    def __init__(self, transaction_id: int, x: int, y: int, z: int) -> None:
        super().__init__()

        self.transaction_id = transaction_id
        self.x, self.y, self.z = x, y, z

    @classmethod
    def decode(cls, buf: Buffer) -> PlayQueryBlockNBT:
        return cls(buf.unpack_varint(), *buf.unpack_pos())


class PlayBlockPlacement(Packet):
    """Sent by the client when it places a block. (Client -> Server)

    :param int hand: The hand used, either main hand (0), or offhand (1).
    :param int x: The x coordinate of the block.
    :param int y: The y coordinate of the block.
    :param int z: The z coordinate of the block.
    :param int face: The face of the block, see here: https://wiki.vg/Protocol#Player_Block_Placement.
    :param float cur_pos_x: The x position of the crosshair on the block.
    :param float cur_pos_y: The y position of the crosshair on the block.
    :param float cur_pos_z: The z position of the crosshair on the block.
    :param bool inside_block: True if the player's head is inside the block.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr hand:
    :attr x:
    :attr y:
    :attr z:
    :attr face:
    :attr cur_pos_x:
    :attr cur_pos_y:
    :attr cur_pos_z:
    :attr inside_block:
    """

    id = 0x2E
    to = 0

    def __init__(
            self,
            hand: int,
            x: int,
            y: int,
            z: int,
            face: int,
            cur_pos_x: float,
            cur_pos_y: float,
            cur_pos_z: float,
            inside_block: bool) -> None:
        super().__init__()

        self.hand = hand
        self.x, self.y, self.z = x, y, z
        self.face = face
        self.cur_pos_x = cur_pos_x
        self.cur_pos_y = cur_pos_y
        self.cur_pos_z = cur_pos_z
        self.inside_block = inside_block

    @classmethod
    def decode(cls, buf: Buffer) -> PlayBlockPlacement:
        return cls(
            buf.unpack_varint(),
            *buf.unpack_pos(),
            buf.unpack_varint(),
            buf.unpack('f'),
            buf.unpack('f'),
            buf.unpack('f'),
            buf.unpack('?')
        )


class PlayNBTQueryResponse(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x54
    to = 1

    def __init__(self, transaction_id: int, nbt: nbt.Tag) -> None:
        super().__init__()

        self.transaction_id = transaction_id
        self.nbt = nbt

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.transaction_id) + Buffer.pack_nbt(self.nbt)
