import random
import uuid

from pymine.api.errors import ParsingError
from pymine.api.abc import AbstractParser


class UUID(AbstractParser):
    def parse(self, s: str) -> tuple:
        try:
            section = s.split()[0]
        except IndexError:
            raise ParsingError

        try:
            return len(section), uuid.UUID(section)
        except ValueError:
            raise ParsingError
