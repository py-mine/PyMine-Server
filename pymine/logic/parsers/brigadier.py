from pymine.api.errors import ParsingError
from pymine.api.abc import AbstractParser

__all__ = ("Bool", "Float", "Double", "Integer", "String")


class Bool(AbstractParser):
    def __init__(self) -> None:
        pass

    def parse(self, s: str) -> tuple:
        if s[:4] == "true":
            return 4, True

        if s[:5] == "false":
            return 5, False

        raise ParsingError


class Float(AbstractParser):
    def __init__(self, min_value: float = -3.4028235e38, max_value: float = 3.4028235e38) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def parse(self, s: str) -> tuple:
        section = s.split(" ")[0]

        try:
            num = float(section)

            if self.min_value is not None and self.max_value > num > self.min_value:
                return len(section), num
        except BaseException:
            pass

        raise ParsingError


class Double(AbstractParser):
    def __init__(self, min_value: float = -1.7976931348623157e307, max_value: float = 1.7976931348623157e307) -> None:
        self.min_value = min_value
        self.max_value = max_value

    @classmethod
    def __getitem__(cls, ranges: slice) -> Double:
        return cls(ranges.start, range.stop)

    def parse(self, s: str) -> tuple:
        try:
            section = s.split()[0]
        except IndexError:
            raise ParsingError

        try:
            num = float(section)
        except ValueError:
            raise ParsingError

        if self.min_value is None or self.max_value > num > self.min_value:
            return len(section), num

        raise ParsingError


class Integer(AbstractParser):
    def __init__(self, min_value: int = -2147483648, max_value: int = 2147483647) -> None:
        self.min_value = min_value
        self.max_value = max_value

    @classmethod
    def __getitem__(cls, ranges: slice) -> Integer:
        return cls(ranges.start, range.stop)

    def parse(self, s: str) -> tuple:
        try:
            section = s.split()[0]
        except IndexError:
            raise ParsingError

        try:
            num = int(section)
        except ValueError:
            raise ParsingError

        if self.min_value is None or self.max_value > num >= self.min_value:
            return len(section), num

        raise ParsingError

class String(AbstractParser):
    def __init__(self, mode: int) -> None:
        self.mode = mode

    @classmethod
    def __getitem__(cls, mode: slice) -> String:
        return cls(mode.start)

    def parse(self, s: str) -> tuple:
        if self.mode == 0:  # single word
            word = s.split(" ")[0]
            return len(word), word

        if self.mode == 1:  # quotable phrase
            if not s[0] == '"':
                raise ParsingError

            out = ""

            for i, c in enumerate(s[1:]):
                if c == '"' and s[i] != "\\":  # allows for escaping of "
                    break

                out += c

            return i + 2, out

        if self.mode == 2:  # rest of string
            return len(s), s

        raise ParsingError
