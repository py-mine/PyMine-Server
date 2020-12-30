"""Contains packets related to blocks."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = (
    'PlayBlockAction',
    'PlayBlockChange',
    'PlayGenerateStructure',
    'PlayQueryBlockNBT',
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

    def __init__(self, x: int, y: int, z: int, action_id: int, action_param: int, block_type: int) -> None:  # nopep8
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


class PlayGenerateStructure(Packet):
    """Sent by the client when the generate button is pressed on a jigsaw block. (Client -> Server)

    :param int x: The x coordinate of the jigsaw block.
    :param int y: The y coordinate of the jigsaw block.
    :param int z: The z coordinate of the jigsaw block.
    :param int levels: The value of the levels slider in the block interface.
    :param bool keep_jigsaws: Unknown.
    :attr type id: Unique packet ID.
    :attr type to: Packet direction.
    :attr x:
    :attr y:
    :attr z:
    :attr levels:
    :attr keep_jigsaws:
    """

    id = 0x0F
    to = 0

    def __init__(self, x: int, y: int, z: int, levels: int, keep_jigsaws: bool):
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.levels = levels
        self.keep_jigsaws = keep_jigsaws

    @classmethod
    def decode(cls, buf: Buffer) -> PlayGenerateStructure:
        return cls(*buf.unpack_pos(), buf.unpack_varint(), buf.unpack_bool())


class PlayQueryBlockNBT(Packet):
    """Used when SHIFT+F3+I is used on a block. (Client -> Server)

    :param int transaction_id: Number used to verify that a response matches.
    :param int x: The x coordinate of the block.
    :param int y: The y coordinate of the block.
    :param int z: The z coordinate of the block.
    :attr type id: Unique packet ID.
    :attr type to: Packet direction.
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
