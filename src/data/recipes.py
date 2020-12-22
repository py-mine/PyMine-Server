import json
import os

__all__ = ('RECIPES',)

RECIPES = {}

for recipe in os.listdir('src/data/recipes'):
    with open('src/data/recipes/' + recipe, 'r') as recipe_file:
        RECIPES[recipe[:5]] = json.load(recipe_file)
