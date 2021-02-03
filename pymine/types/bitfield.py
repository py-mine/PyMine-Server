from __future__ import annotations


class SingleByteBitField:
    def __init__(self, length: int, field: int):
        self.length = length
        self.field = field

    @classmethod
    def from_bools(cls, *values: bool) -> SingleByteBitField:
        field = 0

        for i, v in enumerate(values):
            i = 2 ** i

            if v:
                field |= i
            else:
                field &= ~i

        return cls(len(values), field)

    def unpack(self) -> tuple:
        return tuple((self.table & i & self.length != 0) for i in range(self.length))
