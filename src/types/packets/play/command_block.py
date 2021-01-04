"""Contains packets related to command blocks."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = (
    'PlayUpdateCommandBlock',
    'PlayUpdateCommandBlockMinecart',
    'PlayGenerateStructure',
)

class PlayUpdateCommandBlock(Packet):
    """Used when a client updates a command block. (Client -> Server)

    :param int x: The x coordinate of the command block.
    :param int y: The y coordinate of the command block.
    :param int z: The z coordinate of the command block.
    :param str command: The command text in the command block.
    :param int mode: The mode which the command block is in. Either sequence (0), auto (1), or redstone (2).
    :param int flags: Other flags, see here: https://wiki.vg/Protocol#Update_Command_Block.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr y:
    :attr z:
    :attr command:
    :attr mode:
    :attr flags:
    """

    id = 0x26
    to = 0

    def __init__(self, x: int, y: int, z: int, command: str, mode: int, flags: int) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.command = command
        self.mode = mode
        self.flags = flags

    @classmethod
    def decode(cls, buf: Buffer) -> PlayUpdateCommandBlock:
        return cls(*buf.unpack_pos(), buf.unpack_string(), buf.unpack_varint(), buf.unpack('b'))


class PlayUpdateCommandBlockMinecart(Packet):
    """Sent when the client updates a command block minecart. (Client -> Server)

    :param int entity_id: The ID of the entity (the minecart).
    :param str command: The command text in the command block.
    :param bool track_output: Whether output from the last command is saved.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr entity_id:
    :attr command:
    :attr track_output:
    """

    id = 0x27
    to = 0

    def __init__(self, entity_id: int, command: str, track_output: bool) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.command = command
        self.track_output = track_output

    @classmethod
    def decode(cls, buf: Buffer) -> PlayUpdateCommandBlockMinecart:
        return cls(buf.unpack_varint(), buf.unpack_string(), buf.unpack_bool())


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
