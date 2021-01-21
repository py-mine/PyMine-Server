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
)


class PlayCraftRecipeRequest(Packet):
    """Sent when a client/player clicks a recipe in the crafting book that is craftable. (Client -> Server)

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
    def decode(cls, buf: Buffer) -> PlayCraftRecipeRequest:
        return cls(buf.unpack("b"), buf.unpack_string(), buf.unpack("?"))


class PlaySetDisplayedRecipe(Packet):
    """Replaces Recipe Book Data, type 0. See here: https://wiki.vg/Protocol#Set_Displayed_Recipe (Client -> Server)

    :param str recipe_id: The identifier for the recipe.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr recipe_id:
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
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr book_id:
    :attr book_open:
    :attr filter_active:
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
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr recipes:
    """

    id = 0x5A
    to = 1

    def __init__(self, recipes: list) -> None:
        super().__init__()

        self.recipes = recipes  # should be the RECIPE map

    def encode(self) -> bytes:
        return b"".join(Buffer.pack_recipe(rid, r) for rid, r in self.recipes.items())
