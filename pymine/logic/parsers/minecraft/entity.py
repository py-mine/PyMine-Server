import random
import uuid

from pymine.api.errors import ParsingError
from pymine.api.abc import AbstractParser

from pymine.util.misc import DualMethod


class UUID(AbstractParser):
    @DualMethod
    def parse(self, s: str) -> tuple:
        section = s.split()[0]

        try:
            return len(section), uuid.UUID(section)
        except ValueError:
            raise ParsingError("invalid value for a UUID provided.")
