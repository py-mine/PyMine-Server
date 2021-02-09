"""Contains packets related to crafting and recipes."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayCraftRecipeRequest",
    "PlaySetDisplayedRecipe",
    "PlaySetRecipeBookState",
    "PlayCraftRecipeResponse",
    "PlayDeclareRecipes",
    "PlayUnlockRecipes",
)


class PlayCraftRecipeRequest(Packet):
    """Sent when a client/player clicks a recipe in the crafting book that is craftable. (Client -> Server)

    :param int window_id: ID of the crafting table window.
    :param str recipe_identifier: The recipe identifier.
    :param bool make_all: Whether maximum amount that can be crafted is crafted.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar window_id:
    :ivar recipe_identifier:
    :ivar make_all:
    """

    id = 0x19
    to = 0

    def __init__(self, window_id: int, recipe_identifier: str, make_all: bool) -> None:
        super().__init__()

        self.window_id = window_id
        self.recipe_identifier = recipe_identifier
        self.make_all = make_all

    @classmethod
    def decode(cls, buf: Buffer) -> PlayCraftRecipeRequest:
        return cls(buf.unpack("b"), buf.unpack_string(), buf.unpack("?"))


class PlaySetDisplayedRecipe(Packet):
    """Replaces Recipe Book Data, type 0. See here: https://wiki.vg/Protocol#Set_Displayed_Recipe (Client -> Server)

    :param str recipe_id: The identifier for the recipe.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar recipe_id:
    """

    id = 0x1E
    to = 0

    def __init__(self, recipe_id: str) -> None:
        super().__init__()

        self.recipe_id = recipe_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySetDisplayedRecipe:
        return cls(buf.unpack_string())


class PlaySetRecipeBookState(Packet):
    """Replaces Recipe Book Data, type 1. See here: https://wiki.vg/Protocol#Set_Recipe_Book_State (Client -> Server)

    :param int book_id: One of the following: crafting (0), furnace (1), blast furnace (2), smoker (3).
    :param bool book_open: Whether the crafting book is open or not.
    :param bool filter_active: Unknown.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar book_id:
    :ivar book_open:
    :ivar filter_active:
    """

    id = 0x1F
    to = 0

    def __init__(self, book_id: int, book_open: bool, filter_active: bool) -> None:
        super().__init__()

        self.book_id = book_id
        self.book_open = book_open
        self.filter_active = filter_active

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySetRecipeBookState:
        return cls(buf.unpack_varint(), buf.unpack("?"), buf.unpack("?"))


class PlayCraftRecipeResponse(Packet):
    """insert fancy docstring here (server -> client)"""

    id = 0x2F
    to = 1

    def __init__(self, window_id: int, recipe_identifier: str) -> None:
        super().__init__()

        self.window_id = window_id
        self.recipe_identifier = recipe_identifier

    def encode(self) -> bytes:
        return Buffer.pack("b", self.window_id) + Buffer.pack_string(self.recipe_identifier)


class PlayDeclareRecipes(Packet):
    """Sends all registered recipes to the client. (Server -> Client)

    :param list recipes: The recipes to be sent, should probably be the RECIPES Map (pymine/data/recipes.py).
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar recipes:
    """

    id = 0x5A
    to = 1

    def __init__(self, recipes: list) -> None:
        super().__init__()

        self.recipes = recipes  # should be the RECIPE map

    def encode(self) -> bytes:
        return b"".join([Buffer.pack_recipe(rid, r) for rid, r in self.recipes.items()])


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
            + b"".join([Buffer.pack_string(rid) for rid in self.recipe_ids_1])
        )

        if self.recipe_ids_2:
            out += Buffer.pack("?", True) + b"".join([Buffer.pack_string(rid) for rid in self.recipe_ids_2])
        else:
            out += Buffer.pack("?", False)

        return out
