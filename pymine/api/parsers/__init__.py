import inspect

from pymine.api.abc import AbstractParser

import pymine.api.parsers.brigadier as brigadier
import pymine.api.parsers.minecraft as minecraft

parsers = (*brigadier.__dict__.values(), *minecraft.__dict__.values(),)
parsers = tuple(p for p in parsers if (inspect.isclass(p) and issubclass(p, AbstractParser)))
