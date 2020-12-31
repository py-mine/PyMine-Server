import json
import os

from src.util.immutable import make_immutable

__all__ = ('TAGS',)

TAGS = {}

# Looks like:
# {
#     "tag_type": {
#         "identifier": [
#             "id1",
#             "id2",
#             ...
#         ],
#         ...
#     },
#     ...
# }

for tag_type in os.listdir('src/data/tags'):
    TAGS[tag_type] = {}

    for tag_file in os.listdir(f'src/data/tags/{tag_type}'):
        with open(f'src/data/tags/{tag_type}/{tag_file}') as f:
            TAGS[tag_type][tag_file[:-5]] = json.load(f)['values']

for tag_type in TAGS:
    for identifier, values in TAGS[tag_type].items():
        new_values = []

        for value in values:
            if value.startswith('#'):
                new_values += TAGS[tag_type][value.split(':')[1]]

        if len(new_values) > 0:
            TAGS[tag_type][identifier] = new_values

print(TAGS['items']['flowers'])
TAGS = make_immutable(TAGS)
