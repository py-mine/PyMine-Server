"""For packets related to structure/jigsaw blocks."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayGenerateStructure', 'PlayUpdateJigsawBlock',)


class PlayGenerateStructure(Packet):
    """Sent by the client when the generate button is pressed on a jigsaw block. (Client -> Server)

    :param int x: The x coordinate of the jigsaw block.
    :param int y: The y coordinate of the jigsaw block.
    :param int z: The z coordinate of the jigsaw block.
    :param int levels: The value of the levels slider in the block interface.
    :param bool keep_jigsaws: Unknown.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
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


class PlayUpdateJigsawBlock(Packet):
    """Sent when done is pressed on a jigsaw block. See here: https://wiki.vg/Protocol#Update_Jigsaw_Block (Client -> Server)

    :param int x: The x coordinate of the jigsaw block.
    :param int y: The y coordinate of the jigsaw block.
    :param int z: The z coordinate of the jigsaw block.
    :param str name: The name.
    :param str target: The target.
    :param str pool: The pool.
    :param str final_state: "Turns into" on the GUI, final_state in NBT.
    :param str joint_type: rollable if the attached piece can be rotated, else aligned.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr y:
    :attr z:
    :attr name:
    :attr target:
    :attr pool:
    :attr final_state:
    :attr joint_type:
    """

    id = 0x29  # Might be 0x28?? See here: https://wiki.vg/Protocol#Update_Jigsaw_Block
    to = 0

    def __init__(
            self,
            x: int,
            y: int,
            z: int,
            name: str,
            target: str,
            pool: str,
            final_state: str,
            joint_type: str) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.name = name
        self.target = target
        self.pool = pool
        self.final_state = final_state
        self.joint_type = joint_type

    @classmethod
    def decode(cls, buf: Buffer) -> PlayUpdateJigsawBlock:
        return cls(*buf.unpack_pos(), *(buf.unpack_string() for _ in range(5)))
