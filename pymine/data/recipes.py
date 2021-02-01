import json
import sys
import os

from pymine.util.immutable import make_immutable

__all__ = ("RECIPES",)

if 'sphinx' in sys.modules:
    os.chdir(os.path.join(os.path.dirname(__file__), "../.."))

RECIPES = {}

for recipe in os.listdir("pymine/data/recipes"):
    with open("pymine/data/recipes/" + recipe, "r") as recipe_file:
        RECIPES[recipe[:-5]] = json.load(recipe_file)

RECIPES = make_immutable(RECIPES)
