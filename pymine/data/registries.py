# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import os

from pymine.util.immutable import make_immutable
from pymine.types.registry import Registry

__all__ = ("ITEM_REGISTRY", "PARTICLE_REGISTRY", "FLUID_REGISTRY", "BLOCK_REGISTRY", "ENTITY_REGISTRY")

with open(os.path.join("pymine", "data", "registries.json"), "r") as registry:  # generated from server jar
    REGISTRY_DATA = make_immutable(json.load(registry))

ITEM_REGISTRY = Registry({k: v["protocol_id"] for k, v in REGISTRY_DATA["minecraft:item"]["entries"].items()})
PARTICLE_REGISTRY = Registry({k: v["protocol_id"] for k, v in REGISTRY_DATA["minecraft:particle_type"]["entries"].items()})
FLUID_REGISTRY = Registry({k: v["protocol_id"] for k, v in REGISTRY_DATA["minecraft:fluid"]["entries"].items()})
BLOCK_REGISTRY = Registry({k: v["protocol_id"] for k, v in REGISTRY_DATA["minecraft:block"]["entries"].items()})
ENTITY_REGISTRY = Registry({k: v["protocol_id"] for k, v in REGISTRY_DATA["minecraft:entity_type"]["entries"].items()})
