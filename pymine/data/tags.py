import json
import os

from pymine.util.immutable import make_immutable

__all__ = ("TAGS",)

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

for tag_type in os.listdir("pymine/data/tags"):
    TAGS[tag_type] = {}

    for tag_file in os.listdir(f"pymine/data/tags/{tag_type}"):
        with open(f"pymine/data/tags/{tag_type}/{tag_file}") as f:
            TAGS[tag_type][tag_file[:-5]] = json.load(f)["values"]


def parse(values: list, tag_type: str):
    new_values = []

    for value in values:
        if value.startswith("#"):
            new_values += TAGS[tag_type][value.split(":")[1]]

    if any(v.startswith("#") for v in new_values):
        return parse(new_values, tag_type)

    return new_values


for tag_type in TAGS:
    for identifier, values in TAGS[tag_type].items():
        new_values = parse(values, tag_type)

        if len(new_values) > 0:
            TAGS[tag_type][identifier] = new_values

TAGS = make_immutable(TAGS)
