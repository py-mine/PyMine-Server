"""Contains packets related to villager NPCs."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlaySelectTrade",
    "PlayTradeList",
)


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


class PlayTradeList(Packet):
    """Sends the list of trades a villager NPC is offering. (Server -> Client)

    :param int window_id: The trading GUI/window that is open.
    :param list trades: The trades to be sent.
    :param int villager_lvl: Level of the villager, one of: novice (1), apprentice (2), journeyman (3), expert (4), master (5).
    :param int xp: Total experience for that villager, 0 if the villager is a wandering one.
    :param bool is_regular: Whether the villager is a normal one or a wandering one.
    :param bool can_restock: True for regular villagers, false for wandering ones.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr window_id:
    :attr trades:
    :attr villager_lvl:
    :attr xp:
    :attr is_regular:
    :attr can_restock:
    """

    id = 0x26
    to = 1

    def __init__(self, window_id: int, trades: list, villager_lvl: int, xp: int, is_regular: bool, can_restock: bool) -> None:
        super().__init__()

        self.window_id = window_id
        # We assume that a trade (entry in trades list) is a dictionary that contains trade data, see here: https://wiki.vg/Protocol#Trade_List
        # This is liable to change in the future as we decide how trades will be stored and loaded
        self.trades = trades
        self.villager_lvl = villager_lvl
        self.xp = xp
        self.is_regular = is_regular
        self.can_restock = can_restock

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.window_id)
            + Buffer.pack("b", len(self.trades))
            + b"".join([Buffer.pack_trade(**trade) for trade in self.trades])
            + Buffer.pack_varint(self.villager_lvl)
            + Buffer.pack_varint(self.xp)
            + Buffer.pack("?", self.is_regular)
            + Buffer.pack("?", self.can_restock)
        )
