from pymine.api.abc import AbstractParser


class Bool(AbstractParser):
    def __init__(self) -> None:
        pass

    def parse(self, pos: int, s: str) -> tuple:
        if s[pos:4] == "true":
            return pos + 4, True

        if s[pos:5] == "false":
            return pos + 5, False

        raise ValueError


class Float(AbstractParser):
    def __init__(self, min_value: float = -3.4028235e38, max_value: float = 3.4028235e38) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def parse(self, pos: int, s: str) -> tuple:
        section = s[pos:].split(" ")[0]

        try:
            num = float(section)

            if self.min_value is not None and self.max_value > num > self.min_value:
                return pos + len(section), num
        except BaseException:
            pass

        raise ValueError


class Double(AbstractParser):
    def __init__(self, min_value: float = -1.7976931348623157e307, max_value: float = 1.7976931348623157e307) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def parse(self, pos: int, s: str) -> tuple:
        section = s[pos:].split(" ")[0]

        try:
            num = float(section)

            if self.min_value is not None and self.max_value > num > self.min_value:
                return pos + len(section), num
        except BaseException:
            pass

        raise ValueError


class Integer(AbstractParser):
    def __init__(self, min_value: int = 3.4028235e38, max_value: int = 3.4028235e38) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def parse(self, pos: int, s: str) -> tuple:
        section = s[pos:].split(" ")[0]

        try:
            num = int(section)

            if self.min_value is not None and self.max_value > num > self.min_value:
                return pos + len(section), num
        except BaseException:
            pass

        raise ValueError
