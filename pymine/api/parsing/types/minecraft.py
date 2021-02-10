import random
import uuid

from pymine.api.abc import AbstractParser


class Entity(AbstractParser):  # players should be a list of Player objects, the currently online players
    def __init__(self, mode: int, players: list) -> None:
        self.mode = mode
        self.players = players

    def parse(self, s: str) -> tuple:
        section = s.split(" ")[0]

        if self.mode == 1:  # Allows usage of selectors
            # currently only basic selectors are supported (nothing like @a[name=Iapetus11])
            if section == "@a":
                return self.players

            if section == "@e":
                raise NotImplementedError

            if section == "@p":
                raise NotImplementedError

            if section == "@s":
                raise NotImplementedError

            if section == "@r":
                return random.choice(self.players)

        for p in self.players:
            if section == p.username:
                return len(section), p

            try:
                if uuid.UUID(section) == p.uuid:
                    return len(section), p
            except BaseException:
                pass

        raise ValueError
