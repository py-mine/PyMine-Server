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
import sys
import os

from pymine.util.immutable import make_immutable
from pymine.types.registry import Registry

__all__ = (
    "ITEM_REGISTRY",
    "PARTICLE_REGISTRY",
    "FLUID_REGISTRY",
    "BLOCK_REGISTRY",
    "ENTITY_REGISTRY",
)

if "sphinx" in sys.modules:
    os.chdir(os.path.join(os.path.dirname(__file__), "../.."))

with open(os.path.join("pymine", "data", "registries.json"), "r") as registry:  # generated from server jar
    REGISTRY = make_immutable(json.load(registry))

ITEM_REGISTRY = Registry(REGISTRY["minecraft:item"]["entries"])
PARTICLE_REGISTRY = Registry(REGISTRY["minecraft:particle_type"]["entries"])
FLUID_REGISTRY = Registry(REGISTRY["minecraft:fluid"]["entries"])
BLOCK_REGISTRY = Registry(REGISTRY["minecraft:block"]["entries"])
ENTITY_REGISTRY = Registry(REGISTRY["minecraft:entity_type"]["entries"])
