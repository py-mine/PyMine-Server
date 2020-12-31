import json

from src.util.immutable import make_immutable

__all__ = (
    'ITEM_REGISTRY',
    'PARTICLE_REGISTRY',
    'FLUID_REGISTRY',
    'BLOCK_REGISTRY',
    'ENTITY_REGISTRY',
)

class Registry:
    def __init__(data: dict):
        self.data = make_immutable({k: v['protocol_id'] for k, v in data.items()})
        self.data_reversed = make_immutable({v: k for k, v in data.items()})

    def encode(self, key: object) -> object:
        return self.data[key]

    def decode(self, value: object) -> object:
        return self.data_reversed[value]

with open('src/data/registries.json') as registry:  # generated from server jar
    REGISTRY = make_immutable(json.load(registry))

ITEM_REGISTRY = Registry(REGISTRY['minecraft:item']['entries'])
PARTICLE_REGISTRY = Registry(REGISTRY['minecraft:particle_type']['entries'])
FLUID_REGISTRY = Registry(REGISTRY['minecraft:fluid']['entries'])
BLOCK_REGISTRY = Registry(REGISTRY['minecraft:block']['entries'])
ENTITY_REGISTRY = Registry(REGISTRY['minecraft:entity_type']['entries'])
