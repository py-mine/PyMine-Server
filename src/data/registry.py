from immutables import Map
import json

__all__ = (
    'REGISTRY',
    'ITEMS_BY_NAME',
    'ITEMS_BY_ID',
)

with open('src/data/registries.json') as registry:  # generated from server jar
    REGISTRY = json.load(registry)

ITEMS_BY_NAME = Map({k: v['protocol_id'] for k, v in REGISTRY['minecraft:item']['entries'].items()})
ITEMS_BY_ID = Map({v: k for k, v in ITEMS_BY_NAME.items()})

PARTICLES_BY_NAME = Map({k: v['protocol_id'] for k, v in REGISTRY['minecraft:particle_type']['entries'].items()})
PARTICLES_BY_ID = Map({v: k for k, v in PARTICLES_BY_NAME.items()})
