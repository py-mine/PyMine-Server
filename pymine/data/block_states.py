import json
import os
import sys

from pymine.util.immutable import make_immutable
from pymine.types.registry import Registry

__all__ = ("BLOCK_STATES",)


def reversed_bs_data(bs_data):
    reverse_data = {}

    for k, block in bs_data.items():
        for sv in block["states"]:
            reverse_data[sv["id"]] = {"name": k, "properties": sv.get("properties", {})}

    return make_immutable(reverse_data)


if "sphinx" in sys.modules:
    os.chdir(os.path.join(os.path.dirname(__file__), "../.."))

with open(os.path.join("pymine", "data", "blocks.json"), "r") as block_data:
    bs_data = make_immutable(json.load(block_data))

BLOCK_STATES = Registry(bs_data, reversed_bs_data(bs_data))
