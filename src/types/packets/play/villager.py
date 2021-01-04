from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlaySelectTrade',)


class PlaySelectTrade(Packet):
    """Used when a player selects a specific trade offered by a villager. (Client -> Server)

    :param int selected_slot: The selected slot in the player's trade inventory.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr selected_slot:
    """

    id = 0x23
    to = 0

    def __init__(self, selected_slot: int) -> None:
        super().__init__()

        self.selected_slot = selected_slot

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySelectTrade:
        return cls(buf.unpack_varint())
