"Contains packets related to recipes."

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayUnlockRecipes",)


class PlayUnlockRecipes(Packet):
    """Unlocks specified locked recipes for the client. (Server -> Client)

    :param int action: The action to be taken, see here: https://wiki.vg/Protocol#Unlock_Recipes.
    :param bool crafting_book_open: If true, then the crafting recipe book will be open when the player opens its inventory.
    :param bool crafting_book_filter_active: If true, then the filtering option is active when the players opens its inventory.
    :param bool smelting_book_open: If true, then the smelting recipe book will be open when the player opens its inventory.
    :param bool smelting_book_filter_active: If true, then the filtering option is active when the players opens its inventory.
    :param bool blast_furnace_book_open: If true, then the blast furnace recipe book will be open when the player opens its inventory.
    :param bool blast_furnace_book_filter_active: If true, then the filtering option is active when the players opens its inventory.
    :param bool smoker_book_open: If true, then the smoker recipe book will be open when the player opens its inventory.
    :param bool smoker_book_filter_active: If true, then the filtering option is active when the players opens its inventory.
    :param list recipe_ids_1: First list of recipe identifiers.
    :param list recipe_ids_2: Second list of recipe identifiers.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr action:
    :attr crafting_book_open:
    :attr crafting_book_filter_active:
    :attr smelting_book_open:
    :attr smelting_book_filter_active:
    :attr blast_furnace_book_open:
    :attr blast_furnace_book_filter_active:
    :attr smoker_book_open:
    :attr smoker_book_filter_active:
    :attr recipe_ids_1:
    :attr recipe_ids_2:
    """

    id = 0x35
    to = 1

    def __init__(
        self,
        action: int,
        crafting_book_open: bool,
        crafting_book_filter_active: bool,
        smelting_book_open: bool,
        smelting_book_filter_active: bool,
        blast_furnace_book_open: bool,
        blast_furnace_book_filter_active: bool,
        smoker_book_open: bool,
        smoker_book_filter_active: bool,
        recipe_ids_1: list,
        recipe_ids_2: list = None,
    ) -> None:
        super().__init__()

        self.action = action
        self.crafting_book_open = crafting_book_open
        self.crafting_book_filter_active = crafting_book_filter_active
        self.smelting_book_open = smelting_book_open
        self.smelting_book_filter_active = self.smelting_book_filter_active
        self.blast_furnace_book_open = blast_furnace_book_open
        self.blast_furnace_book_filter_active = blast_furnace_book_filter_active
        self.smoker_book_open = smoker_book_open
        self.smoker_book_filter_active = smoker_book_filter_active
        self.recipe_ids_1 = recipe_ids_1
        self.recipe_ids_2 = recipe_ids_2

    def encode(self) -> bytes:
        out = (
            Buffer.pack_varint(self.action)
            + Buffer.pack("?", self.crafting_book_open)
            + Buffer.pack("?", self.crafting_book_filter_active)
            + Buffer.pack("?", self.smelting_book_open)
            + Buffer.pack("?", self.smelting_book_filter_active)
            + Buffer.pack("?", self.blast_furnace_book_open)
            + Buffer.pack("?", self.blast_furnace_book_filter_active)
            + Buffer.pack("?", self.smoker_book_open)
            + Buffer.pack("?", self.smoker_book_filter_active)
            + Buffer.pack_varint(len(self.recipe_ids_1))
            + b"".join(Buffer.pack_string(rid) for rid in self.recipe_ids_1)
        )

        if self.recipe_ids_2:
            out += Buffer.pack("?", True) + b"".join(Buffer.pack_string(rid) for rid in self.recipe_ids_2)
        else:
            out += Buffer.pack("?", False)

        return out
