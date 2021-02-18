from __future__ import annotations

import immutables
import math

from pymine.types.registry import Registry
import pymine.types.nbt as nbt

from pymine.data.block_states import BLOCK_STATES

from pymine.api.abc import AbstractPalette


class DirectPalette(AbstractPalette):
    @staticmethod
    def get_bits_per_block():
        return math.ceil(math.log2(sum(len(b["states"]) for b in BLOCK_STATES.items())))  # should be 14 or 15

    @staticmethod
    def encode(block: str, props: dict = None) -> int:
        block_data = BLOCK_STATES.encode(block)

        for state in block_data["states"]:
            if not props and state.get("default"):
                return state["id"]

            state_props = state.get("properties")

            if state_props and dict(state_props.items()) == props:
                return state["id"]

        raise ValueError(f"{block} doesn't have a state with those properties.")

    @staticmethod
    def decode(state: int) -> immutables.Map:
        return BLOCK_STATES.decode(state)


class IndirectPalette(AbstractPalette):
    def __init__(self, registry: Registry) -> None:
        self.registry = registry

    @classmethod
    def from_nbt(cls, tag: nbt.TAG) -> IndirectPalette:
        # TAG_List("Palette"): [
        #     TAG_Compound(""): [
        #         TAG_String("Name"): minecraft:air
        #     ],
        #     TAG_Compound(""): [
        #         TAG_String("Name"): minecraft:grass_block,
        #         TAG_Compound("Properties"): [
        #             TAG_String("snowy"): false
        #         ]
        #     ],
        #     TAG_Compound(""): [
        #         TAG_String("Name"): minecraft:cut_sandstone
        #     ]
        # ]

        reverse_data = {}

        for i, b in enumerate(tag):
            reverse_data[i] = {"name": tag["Name"], "properties": {k: v for k, v in tag["Properties"]}}

    def encode(self, block: str, props: dict = None) -> int:
        block_data = self.registry.encode(block)

        for state in block_data["states"]:
            if not props and state.get("default"):
                return state["id"]

            state_props = state.get("properties")

            if state_props and dict(state_props.items()) == props:
                return state["id"]

        raise ValueError(f"{block} doesn't have a state with those properties.")

    def decode(self, state: int) -> immutables.Map:
        return self.registry.decode(state)
