"""Contains packets related to command blocks."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayUpdateCommandBlock',)

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
