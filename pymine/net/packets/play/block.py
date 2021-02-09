"""Contains packets related to blocks."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt

__all__ = (
    "PlayBlockAction",
    "PlayBlockChange",
    "PlayQueryBlockNBT",
    "PlayBlockPlacement",
    "PlayNBTQueryResponse",
    "PlayMultiBlockChange",
)


class PlayBlockAction(Packet):
    """This packet is used for a number of actions and animations performed by blocks. (Server -> Client)

    :param int x: The x coordinate of the location where this occurs.
    :param int y: The y coordinate of the location where this occurs.
    :param int z: The z coordinate of the location where this occurs.
    :param int action_id: Block action ID, see here: https://wiki.vg/Block_Actions.
    :param int action_param: Action param of the action, see here: https://wiki.vg/Block_Actions.
    :param int block_type: The type of block which the action is for.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar action_id:
    :ivar action_param:
    :ivar block_type:
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
        return (
            Buffer.pack_pos(self.x, self.y, self.z)
            + Buffer.pack("B", self.action_id)
            + Buffer.pack("B", self.action_param)
            + Buffer.pack_varint(self.block_type)
        )


class PlayBlockChange(Packet):
    """Fired when a block is changed within the render distance. (Server -> Client)

    :param int x: The x coordinate of the location where this occurs.
    :param int y: The y coordinate of the location where this occurs.
    :param int z: The z coordinate of the location where this occurs.
    :param int block_id: Block ID of what to change the block to.
    :ivar int id: Unique packet ID.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar block_id:
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
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar transaction_id:
    :ivar x:
    :ivar y:
    :ivar z:
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
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar hand:
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar face:
    :ivar cur_pos_x:
    :ivar cur_pos_y:
    :ivar cur_pos_z:
    :ivar inside_block:
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
        inside_block: bool,
    ) -> None:
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
            buf.unpack("f"),
            buf.unpack("f"),
            buf.unpack("f"),
            buf.unpack("?"),
        )


class PlayNBTQueryResponse(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x54
    to = 1

    def __init__(self, transaction_id: int, nbt: nbt.TAG) -> None:
        super().__init__()

        self.transaction_id = transaction_id
        self.nbt = nbt

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.transaction_id) + Buffer.pack_nbt(self.nbt)


class PlayMultiBlockChange(Packet):
    """Sent whenever 2 or more blocks change in the same chunk on the same tick. (Server -> Client)

    :param int chunk_sect_x: The x coordinate of the chunk section.
    :param int chunk_sect_y: The y coordinate of the chunk section.
    :param int chunk_sect_z: The z coordinate of the chunk section.
    :param bool trust_edges: The inverse of preceding PlayUpdateLight packet's trust_edges bool
    :param list blocks: The changed blocks, formatted like [block_id, local_x, local_y, local_z].
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar chunk_sect_x:
    :ivar chunk_sect_y:
    :ivar chunk_sect_z:
    :ivar trust_edges:
    :ivar blocks:
    """

    id = 0x3B
    to = 1

    def __init__(self, chunk_sect_x: int, chunk_sect_y: int, chunk_sect_z: int, trust_edges: bool, blocks: list) -> None:
        super().__init__()

        self.chunk_sect_x = chunk_sect_x
        self.chunk_sect_y = chunk_sect_y
        self.chunk_sect_z = chunk_sect_z
        self.trust_edges = trust_edges
        self.blocks = blocks

    def encode(self) -> bytes:
        out = (
            Buffer.pack_varint(
                ((self.chunk_sect_x & 0x3FFFFF) << 42) | (self.chunk_sect_y & 0xFFFFF) | ((self.chunk_sect_z & 0x3FFFFF) << 20)
            )
            + Buffer.pack("?", self.trust_edges)
            + Buffer.pack_varint(len(self.blocks))
        )

        for block_id, local_x, local_y, local_z in self.blocks:
            out += Buffer.pack_varint(block_id << 12 | (local_x << 8 | local_z << 4 | local_y))

        return out
