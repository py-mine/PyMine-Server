from pymine.api.abc import AbstractParser

class Bool(AbstractParser):
    @staticmethod
    def parse(pos: int, s: str) -> tuple:
        if s[pos:4] == "true":
            return pos + 4, True

        if s[pos:5] == "false":
            return pos + 5, False

        raise ValueError


class Float(AbstractParser):
    @staticmethod
    def parse(pos: int, s: str) -> tuple:
        section = s.split(' ')[0]

        try:
            return pos + len(section), float(section)
        except BaseException:
            pass

        raise ValueError


class Double(AbstractParser):
    @staticmethod
    def parse(pos: int, s: str) -> tuple:
        section = s.split(' ')[0]

        try:
            return pos + len(section), float(section)
        except BaseException:
            pass

        raise ValueError


class Integer(AbstractParser):
    @staticmethod
    def parse(pos: int, s: str) -> tuple:
        section = s.split(' ')[0]

        try:
            return pos + len(section), int(section)
        except BaseException:
            pass

        raise ValueError
