from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('CraftRecipeRequest',)


class CraftRecipeRequest(Packet):
    """Sent when a client/player clicks a recipe in the crafting book that is craftable.

    :param int window_id: ID of the crafting table window.
    :param str recipe_identifier: The recipe identifier.
    :param bool make_all: Whether maximum amount that can be crafted is crafted.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr window_id:
    :attr recipe_identifier:
    :attr make_all:
    """

    id = 0x19
    to = 0

    def __init__(self, window_id: int, recipe_identifier: str, make_all: bool) -> None:
        super().__init__()

        self.window_id = window_id
        self.recipe_identifier = recipe_identifier
        self.make_all = make_all

    @classmethod
    def decode(cls, buf: Buffer):
        return cls(buf.unpack('b'), buf.unpack_string(), buf.unpack_bool())
