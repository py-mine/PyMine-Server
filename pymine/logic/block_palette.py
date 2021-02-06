import immutables
import math

from pymine.data.block_states import BLOCK_STATES

class DirectPalette:
    @staticmethod
    def get_bits_per_block():
        return math.ceil(math.log2(sum(len(b["states"]) for b in BLOCK_STATES.items())))  # should be 14 or 15

    @staticmethod
    def encode(block: str, props: dict) -> int:
        block_data = BLOCK_STATES.encode(block)

        for state in block_data["states"]:
            if dict(state["properties"]) == props:
                return state["id"]

        raise ValueError(f"{block} doesn't have a state with those properties.")

    @staticmethod
    def decode(state: int) -> immutables.Map:
        return BLOCK_STATES.decode(state)
