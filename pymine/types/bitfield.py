from __future__ import annotations


class BitField:
    def __init__(self, length: int, field: int):
        self.length = length
        self.field = field

    @classmethod
    def from_values(cls, *values: bool) -> BitField:
        field = 0

        for i, v in enumerate(values):
            if v:
                field |= 2**i
            else:
                field &= ~(2**i)

        return cls(len(values), field)

    def unpack(self) -> tuple:
        return tuple((self.field >> i) & 1 for i in range(self.length))

    def __str__(self):
        return f"BoolBitField(0x{self.field:0X}, length={self.length})"
