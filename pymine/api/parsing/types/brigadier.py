from pymine.api.abc import AbstractParser

class Bool(AbstractParser):
    @staticmethod
    def parse(pos: int, s: str) -> tuple:
        if s[pos:4] == "true":
            return pos + 4, True

        if s[pos:5] == "false":
            return pos + 5, False

        raise ValueError
