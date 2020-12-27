"""Contains packets related to players."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayAcknowledgePlayerDigging',)


class PlayAcknowledgePlayerDigging(Packet):
    """Sent by server to acknowledge player digging. (Server -> Client)

    :param int x: The x coordinate of where the player is digging.
    :param int y: The y coordinate of where the player is digging.
    :param int z: The z coordinate of where the player is digging.
    :param int block: The block state id of the block that is being broken/dug.
    :param int status: Value 0-2 to denote whether player should start, cancel, or finish.
    :param bool successful: True if the block was dug successfully.
    :attr int id_: Unique packet ID.
    :attr x:
    :attr y:
    :attr z:
    :attr block:
    :attr status:
    :attr successful:
    """

    id_ = 0x07
    to = 1

    def __init__(self, x: int, y: int, z: int, block: int, status: int, successful: bool) -> None:
        super().__init__()

        self.x = x
        self.y = y
        self.z = z
        self.block = block
        self.status = status
        self.successful = successful

    def encode(self) -> bytes:
        return Buffer.pack_pos(self.x, self.y, self.z) + \
            Buffer.pack_varint(self.block) + \
            Buffer.pack_varint(self.status) + \
            Buffer.pack_bool(self.successful)
