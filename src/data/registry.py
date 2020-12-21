import json

__all__ = (
    'REGISTRY',
    'ITEMS'
)

with open('registries.json') as registry:  # generated from server jar
    REGISTRY = json.load(registry)

ITEMS_BY_NAME = REGISTRY['minecraft:item']['entries']
ITEMS_BY_ID = {v: k for k, v in ITEMS_BY_NAME.items()}
