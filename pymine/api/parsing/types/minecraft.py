import uuid

from pymine.api.abc import AbstractParser


class Entity(AbstractParser):  # players should be a list of Player objects, the currently online players
    def __init__(self, mode: int, players: list) -> None:
        self.mode = mode
        self.players = players

    def parse(self, s: str) -> tuple:
        section = s.split(" ")[0]

        if self.mode == 1:  # "If set, only allows a single entity/player"
            raise NotImplementedError

        if self.mode == 2:
            for p in players:
                if section == p.username:
                    return len(section), p

                try:
                    if uuid.UUID(section) == p.uuid:
                        return len(section), p
                except BaseException:
                    pass

        raise ValueError
