import json
import os

from pymine.util.immutable import make_immutable
from pymine.types.registry import Registry

__all__ = (
    "ITEM_REGISTRY",
    "PARTICLE_REGISTRY",
    "FLUID_REGISTRY",
    "BLOCK_REGISTRY",
    "ENTITY_REGISTRY",
)

with open(os.path.join("pymine", "data", "registries.json"), "r") as registry:  # generated from server jar
    REGISTRY = make_immutable(json.load(registry))

ITEM_REGISTRY = Registry(REGISTRY["minecraft:item"]["entries"])
PARTICLE_REGISTRY = Registry(REGISTRY["minecraft:particle_type"]["entries"])
FLUID_REGISTRY = Registry(REGISTRY["minecraft:fluid"]["entries"])
BLOCK_REGISTRY = Registry(REGISTRY["minecraft:block"]["entries"])
ENTITY_REGISTRY = Registry(REGISTRY["minecraft:entity_type"]["entries"])
