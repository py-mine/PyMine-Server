from random import randint
import functools
import asyncio
import hashlib
import types

# An implementation of java's String.hashCode()
def java_string_hash(s: str) -> int:
    l = len(s)
    return sum((ord(s[i]) * 31 ** (l - 1 - i) for i in range(l))) & 0xFFFFFFFF


def gen_seed() -> int:  # generates a random seed as an int
    return randint(0, (2 ** 64) - 1)


# May not be correct, but it doesn't matter because it's used for "biome noise" client-side
def seed_hash(seed: int):
    m = hashlib.sha256()
    m.update(seed.to_bytes(8, "big"))
    return int(str(int.from_bytes(m.digest(), "big"))[:8])


def remove_namespace(s: str) -> str:
    if ":" in s:
        return "".join(s.split(":")[1:])

    return s


class DualMethod:
    """Allows a method of a class to be a classmethod or regular method.
    If the method is called like Class.method(), the first parameter will be the class object.
    If the method is called like instance.method(), the first parameter will be the instance of the class object.

    Usage is like:
    class Foo:
        @DualMethod
        def bar(self, *args):
            print(*args)
    """

    def __init__(self, func):
        self._func = func

    def __get__(self, instance, owner=None):
        return types.MethodType(self._func, (owner if instance is None else instance))
