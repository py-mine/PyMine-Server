import json

__all__ = (
    'REGISTRY',
    'ITEMS'
)

with open('registries.json') as registry:  # generated from server jar
    REGISTRY = json.load(registry)

ITEMS = REGISTRY['minecraft:item']['entries']
