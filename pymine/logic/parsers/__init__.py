import classyjson
import importlib
import os

parsers = classyjson.ClassyDict()

for root, dirs, files in os.walk(os.path.join("pymine", "logic", "parsers")):
    for file in filter((lambda f: f.endswith(".py")), files):
        module = importlib.import_module(os.path.join(root, file)[:-3].replace("\\", "/").replace("/", "."))

        for name, obj in module.__dict__.items():
            if issubclass(obj, AbstractParser):
                parsers[name] = obj
