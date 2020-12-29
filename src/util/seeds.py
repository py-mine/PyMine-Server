from random import random

__all__ = ('string_hash_code', 'gen_seed',)


def string_hash_code(s: str):
    n = len(s)
    hash_code = 0

    for i, c in enumerate(s, start=1):
        hash_code += c * (31 ** (n - i))

    return hash_code


def gen_seed():
    return random() * (2 ** 64)
