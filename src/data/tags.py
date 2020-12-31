import json
import os

from src.util.immutable import make_immutable

__all__ = ('TAGS',)

TAGS = {}

for tag_type in os.listdir('src/data/tags'):
    TAGS[tag_type] = {}
    
    for tag_file in os.listdir(f'src/data/tags/{tag_type}'):
        with open(f'src/data/tags/{tag_type}/{tag_file}') as f:
            TAGS[tag_type][tag_file[:-5]] = json.load(f)['values']

TAGS = make_immutable(TAGS)
