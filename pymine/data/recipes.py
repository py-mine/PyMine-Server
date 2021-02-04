import json
import sys
import os

from pymine.util.immutable import make_immutable

__all__ = ("RECIPES",)

if "sphinx" in sys.modules:
    os.chdir(os.path.join(os.path.dirname(__file__), "../.."))

RECIPES = {}
RECIPE_DIR = os.path.join("pymine", "data", "recipes")

for recipe in os.listdir(RECIPE_DIR):
    with open(os.path.join(RECIPE_DIR, recipe), "r") as recipe_file:
        RECIPES[recipe[:-5]] = json.load(recipe_file)

RECIPES = make_immutable(RECIPES)
