import uuid

from pymine.api.abc import AbstractParser
from pymine.server import server


class UUID(AbstractParser):
    def __init__(self) -> None:
        pass

    def parse(self, s: str) -> tuple:
        section = s.split()[0]

        return len(section), server.playerio.cache[int(uuid.UUID(section))]
