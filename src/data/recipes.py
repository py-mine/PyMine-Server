import json
import os

__all__ = ['RECIPES']

RECIPES = {}

for recipe in os.listdir('src/data/recipes'):
    print('getting recipe')
    with open(recipe, 'r') as recipe_file:
        RECIPES[recipe[:5]] = json.load(recipe_file)
