from __future__ import annotations


class BoolBitField:
    def __init__(self, length: int, field: int):
        self.length = length
        self.field = field

    @classmethod
    def from_bools(cls, *values: bool) -> BoolBitField:
        field = 0

        for i, v in enumerate(values):
            i = 2 ** i

            if v:
                field |= i
            else:
                field &= ~i

        return cls(len(values), field)

    def unpack(self) -> tuple:
        return tuple((self.field & i & self.length != 0) for i in range(self.length))

    def __str__(self):
        return f"BoolBitField(0x{self.field:0X}, length={self.length})"
