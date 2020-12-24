import json

__all__ = (
    'REGISTRY',
    'ITEMS_BY_NAME',
    'ITEMS_BY_ID',
)

with open('src/data/registries.json') as registry:  # generated from server jar
    REGISTRY = json.load(registry)

ITEMS_BY_NAME = {k: tuple(v) for k, v in REGISTRY['minecraft:item']['entries'].items()}
ITEMS_BY_ID = {v: k for k, v in ITEMS_BY_NAME.items()}
