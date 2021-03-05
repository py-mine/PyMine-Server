from random import randint
import functools
import asyncio
import hashlib


def string_hash_code(s: str) -> int:  # implementation of java's String.hashCode()
    n = len(s)
    hash_code = 0

    for i, c in enumerate(s, start=1):
        hash_code += c * (31 ** (n - i))

    return hash_code


def gen_seed() -> int:  # generates a random seed as an int
    return randint(0, (2 ** 64) - 1)


def seed_hash(seed: int):  # probably not correct but it seems to work so?
    m = hashlib.sha256()
    m.update(seed.to_bytes(8, "big"))
    return int(str(int.from_bytes(m.digest(), "big"))[:8])


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
