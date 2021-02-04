from __future__ import annotations


class BitField:
    """Used to store boolean flags based on their values. If I were to create a bit field with flags 1 and 2, getting those flags would return True and True, getting a flag that wasn't put in results in a False

    :param int length: Length of the bit field.
    :param int field: The actual field data (as an int).
    :ivar length:
    :ivar field:
    """

    def __init__(self, length: int, field: int) -> None:
        self.length = length
        self.field = field

    @classmethod  # [(flag, bool), (flag, bool)]
    def new(cls, length: int, *flags) -> BitField:
        field = 0

        for flag in flags:
            if flag[1]:
                field |= 2 ** flag[0]
            else:
                field &= ~flag[0]

        return cls(length, field)

    def add(self, flag: int, state: bool) -> None:
        if state:
            self.field |= 2 ** flag
        else:
            self.field &= ~flag

    def get(self, flag: int) -> int:
        return (self.field >> flag) & 1

    def get_flags(self, *flags: int) -> tuple:
        return [self.get(flag) for flag in flags]

    def __str__(self) -> str:
        return str(self.field)

    def __repr__(self) -> str:
        return f"BitField(0x{self.field:0X}, length={self.length})"


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
