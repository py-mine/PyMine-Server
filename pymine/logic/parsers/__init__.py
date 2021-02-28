from pymine.logic.parsers.brigadier import *
from pymine.logic.parsers.minecraft import *


# parsers = []
#
# for root, dirs, files in os.walk(os.path.join("pymine", "api", "parsers")):
#     for file in files:
#         if file.endswith(".py"):
#             module = importlib.import_module(os.path.join(root, file[:-3]).replace("\\", "/").replace("/", "."))
#             parsers += [
#                 p
#                 for p in module.__dict__.values()
#                 if (inspect.isclass(p) and p is not AbstractParser and issubclass(p, AbstractParser))
#             ]
