import random
import uuid

from pymine.api.errors import ParsingError
from pymine.api.abc import AbstractParser

from pymine.server import server


class UUID(AbstractParser):
    def parse(self, s: str) -> tuple:
        try:
            section = s.split()[0]
        except IndexError:
            raise ParsingError

        try:
            return len(section), uuid.UUID(section)
        except ValueError:  # valueerror for if section isn't valid uuid, keyerror for if player isn't in cache
            raise ParsingError

class Player(AbstractParser):
    def parse(self, s: str) -> tuple:
        try:
            section = s.split()[0]
        except IndexError:
            raise ParsingError

        try:
            return len(section), server.playerio.cache[int(uuid.UUID(section))]
        except (ValueError, KeyError):  # valueerror for if section isn't valid uuid, keyerror for if player isn't in cache
            raise ParsingError
