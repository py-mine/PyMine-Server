class Bool:
    @staticmethod
    def parse(s: str) -> bool:
        if s == "true":
            return True

        if s == "false":
            return False

        raise ValueError


class Double:
    @staticmethod
    def parse(s: str, max_=1.7976931348623157e307, min_=-1.7976931348623157e307) -> float:
        try:
            value = float(s)

            if max_ >= value >= min_:
                return value
        except BaseException:
            pass

        raise ValueError


class Float:
    @staticmethod
    def parse(s: str, max_=3.4028235e38, min_=-3.4028235e38) -> float:
        try:
            value = float(s)

            if max_ >= value >= min_:
                return value
        except BaseException:
            pass

        raise ValueError


class Integer:
    @staticmethod
    def parse(s: str, max_=2147483647, min_=-2147483648) -> int:
        try:
            value = int(s)

            if max_ >= value >= min_:
                return value
        except BaseException:
            pass

        raise ValueError


class String:
    @staticmethod
    def parse(s: str, type_: int) -> str:
        out = ""

        if type_ == 0:
            for c in s:
                if c == " " or c == '"':
                    break

                out += c
        elif type_ == 1:
            pass
