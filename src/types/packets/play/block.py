"""Contains packets related to entitys."""

from __future__ import annotations

from src.types.packet import Packet

__all__ = ('PlayBlockAction', 'PlayBlockChange',)


class PlayBlockAction(Packet):
    """This packet is used for a number of actions and animations performed by blocks. (Server -> Client)

    :param dict response_data: Description of parameter `response_data`.
    :attr type id_: Description of parameter `id_`.
    """

    id_ = 0x0A

    def __init__(self, x: int, y: int, z: int, action_id: int, action_param: int, block_type: int) -> None:
        super().__init__()

        self.x = x
        self.y = y
        self.z = z
        self.action_id = action_id
        self.action_param = action_param
        self.block_type = block_type

    def encode(self) -> bytes:
        return Buffer.pack_pos(self.x, self.y, self.z) + \
         Buffer.pack('B', self.action_id) + \
         Buffer.pack('B', self.action_param) + \
         Buffer.pack_varint(self.block_type)


class PlayBlockChange(Packet):
    """Fired when a block is changed within the render distance. Client bound(Client -> Server)."""

    id_ = 0x0B

    def __init__(self, response_data: dict) -> None:
        super().__init__()
