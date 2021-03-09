from pymine.api.errors import ParsingError
from pymine.types.abc import AbstractParser

from pymine.util.misc import DualMethod

__all__ = ("Bool", "Float", "Double", "Integer", "String")


class Bool(AbstractParser):
    @DualMethod
    def parse(self, s: str) -> tuple:
        if s[:4] == "true":
            return 4, True

        if s[:5] == "false":
            return 5, False

        raise ParsingError("invalid value for a bool provided, use either true or false.")


class Float(AbstractParser):
    min_value = -3.4028235e38
    max_value = 3.4028235e38

    def __init__(self, min_value: float = min_value, max_value: float = max_value) -> None:
        self.min_value = min_value
        self.max_value = max_value

    @DualMethod
    def parse(self, s: str) -> tuple:
        section = s.split()[0]

        try:
            num = float(section)
        except ValueError:
            raise ParsingError("invalid value provided for a number.")

        if self.min_value is None or self.max_value > num > self.min_value:
            return len(section), num

        raise ParsingError(f"provided value is not within allowed range ({self.min_value} < value < {self.max_value}).")


class Double(AbstractParser):
    min_value = -1.7976931348623157e307
    max_value = 1.7976931348623157e307

    def __init__(self, min_value: float = min_value, max_value: float = max_value) -> None:
        self.min_value = min_value
        self.max_value = max_value

    @DualMethod
    def parse(self, s: str) -> tuple:
        section = s.split()[0]

        try:
            num = float(section)
        except ValueError:
            raise ParsingError("invalid value provided for a number.")

        if self.min_value is None or self.max_value > num > self.min_value:
            return len(section), num

        raise ParsingError(f"provided value is not within allowed range ({self.min_value} < value < {self.max_value}).")


class Integer(AbstractParser):
    min_value = -2147483648
    max_value = 2147483647

    def __init__(self, min_value: int = min_value, max_value: int = max_value) -> None:
        self.min_value = min_value
        self.max_value = max_value

    @DualMethod
    def parse(self, s: str) -> tuple:
        section = s.split()[0]

        try:
            num = int(section)
        except ValueError:
            raise ParsingError("invalid value provided for an integer number.")

        if self.min_value is None or self.max_value > num >= self.min_value:
            return len(section), num

        raise ParsingError(f"provided value is not within allowed range ({self.min_value} < value < {self.max_value}).")


class String(AbstractParser):
    mode = 0

    def __init__(self, mode: int) -> None:
        self.mode = mode

    @DualMethod
    def parse(self, s: str) -> tuple:
        if self.mode == 0:  # single word
            word = s.split()[0]
            return len(word), word

        if self.mode == 1:  # quotable phrase
            if not s[0] == '"':
                raise ParsingError("missing starting quotes.")

            out = ""

            for i, c in enumerate(s[1:]):
                if c == '"' and s[i] != "\\":  # allows for escaping of "
                    out += '"'
                    break

                out += c

            if not out.endswith('"'):
                raise ParsingError("missing closing quotes.")

            return i + 2, out[:-1]

        if self.mode == 2:  # rest of string
            return len(s), s

        raise ParsingError(f"failed to parse a string in mode {self.mode}.")
