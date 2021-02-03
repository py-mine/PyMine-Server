from __future__ import annotations


# class BoolBitField:
#     def __init__(self, length: int, field: int):
#         self.length = length
#         self.field = field
#
#     @classmethod
#     def from_values(cls, *values: bool) -> BoolBitField:
#         field = 0
#
#         for i, v in enumerate(values):
#             if v:
#                 field |= 2 ** i
#             else:
#                 field &= ~(2 ** i)
#
#         return cls(len(values), field)
#
#     def get_values(self) -> tuple:
#         return tuple(bool((self.field >> i) & 1) for i in range(self.length))
#
#     def __str__(self):
#         return str(self.unpack())
#
#     def __repr__(self):
#         return f"BitField(0x{self.field:0X}, length={self.length})"


class BitField:
    def __init__(self, length: int, field: int):
        self.length = length
        self.field = field

    @classmethod
    def from_flags(cls, length: int, *flags: int) -> BitField:
        field = 0

        for flag in flags:
            field |= 2 ** flag

        return cls(length, field)

    def get(self, flag: int):
        return (self.field >> flag) & 1

    def get_flags(self, *flags: int) -> tuple:
        return [self.get(flag) for flag in flags]
