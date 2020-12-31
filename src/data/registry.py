from immutables import Map
import json

__all__ = (
    'REGISTRY',
    'ITEMS_BY_NAME',
    'ITEMS_BY_ID',
    'PARTICLES_BY_NAME',
    'PARTICLES_BY_ID',
)

class Registry:
    def __init__(data: dict):
        self.data = Map(data)
        self.data_reversed = Map({v: k for k, v in data.items()})

    def encode(self, key: object) -> object:
        return self.data[key]

    def decode(self, value: object) -> object:
        return self.data_reversed[value]

with open('src/data/registries.json') as registry:  # generated from server jar
    REGISTRY = json.load(registry)

ITEMS_BY_NAME = Map({k: v['protocol_id'] for k, v in REGISTRY['minecraft:item']['entries'].items()})
ITEMS_BY_ID = Map({v: k for k, v in ITEMS_BY_NAME.items()})

PARTICLES_BY_NAME = Map({k: v['protocol_id']
                         for k, v in REGISTRY['minecraft:particle_type']['entries'].items()})
PARTICLES_BY_ID = Map({v: k for k, v in PARTICLES_BY_NAME.items()})

FLUIDS_BY_NAME = Map({k: v['protocol_id'] for k, v in REGISTRY['minecraft:fluid']['entries'].items()})
FLUIDS_BY_ID = Map({v: k for k, v in FLUIDS_BY_NAME.items()})
