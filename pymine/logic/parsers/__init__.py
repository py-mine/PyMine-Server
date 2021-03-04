import classyjson
import importlib
import os

from pymine.api.abc import AbstractParser

parsers = classyjson.ClassyDict()

for root, dirs, files in os.walk(os.path.join("pymine", "logic", "parsers")):
    for file in filter((lambda f: f.endswith(".py") and "__" not in f), files):
        module = importlib.import_module(os.path.join(root, file)[:-3].replace("\\", "/").replace("/", "."))

        for name, obj in module.__dict__.items():
            try:
                if issubclass(obj, AbstractParser):
                    parsers[name] = obj
            except (TypeError, KeyError):  # can't call issubclass() on non-classes
                pass
