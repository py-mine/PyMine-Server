import random
import uuid

from pymine.api.errors import ParsingError
from pymine.api.abc import AbstractParser

from pymine.server import server


class Player(AbstractParser):
    def parse(self, s: str) -> tuple:
        try:
            section = s.split()[0]
        except IndexError:
            raise ParsingError

        # check if section could be a valid username
        if 17 > len(section) > 1 and section.lower().strip("abcdefghijklmnopqrstuvwxyz1234567890_") == "":
            for player in server.playerio.cache.values():
                if player.username == section:
                    return len(section), player

        # check if section could be a valid uuid
        if len(section) in (32, 36) and section.lower().strip("abcdefghijklmnopqrstuvwxyz1234567890-") == "":
            try:
                return len(section), server.playerio.cache[int(uuid.UUID(section))]
            except (ValueError, KeyError):  # valueerror for if section isn't valid uuid, keyerror for if player isn't in cache
                pass

        raise ParsingError
