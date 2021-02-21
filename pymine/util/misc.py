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


# def run_in_executor(func):
#     @functools.wraps(func)
#     def deco(*args, **kwargs):
#         return asyncio.get_running_loop().run_in_executor(None, functools.partial(func, *args, **kwargs))
#
#     return deco
