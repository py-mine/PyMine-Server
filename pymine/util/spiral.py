from math import isqrt


def first(cycle: int):
    return (2 * cycle - 1) ** 2


def cycle(index: int):
    return (isqrt(index) + 1) // 2


def length(cycle: int):
    return 8 * cycle


def sector(index: int):
    c = cycle(index)

    return 4 * (index - first(c)) / length(c)


def position(index: int):
    c = cycle(index)
    s = sector(index)

    offset = index - first(c) - s * length(c) // 4

    if s == 0:  # north
        return -c, -c + offset + 1

    if s == 1:  # east
        return -c + offset + 1, c

    if s == 2:  # south
        return c, c - offset - 1

    # else, west
    return c - offset - 1, -c

def spiral(iterable):
    for i in range(len(iterable)):
        yield iterable[position(i)]
