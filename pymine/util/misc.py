from random import randint
import functools
import itertools
import asyncio
import hashlib
import types
import ast


def spiral(chunks: dict):
    def spiral_(l):
        while l:
            yield l[0]
            l = list(reversed(list(zip(*l[1:]))))

    spiraled = list(itertools.chain.from_iterable(spiral_(list(chunks.items()))))
    out = {}

    for i in range(0, len(spiraled), 2):
        out[spiraled[i]] = spiraled[i + 1]

    return out


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


async def nice_eval(code: str, env: dict) -> str:
    code_nice = f"async def nice_eval():\n" + "\n".join(f"    {i}" for i in code.strip(" `py\n ").splitlines())
    code_parsed = ast.parse(code_nice)
    code_final = code_parsed.body[0].body

    def insert_returns():
        if isinstance(code_final[-1], ast.Expr):
            code_final[-1] = ast.Return(code_final[-1].value)
            ast.fix_missing_locations(code_final[-1])

        if isinstance(code_final[-1], ast.If):
            insert_returns(code_final[-1].body)
            insert_returns(code_final[-1].orelse)

        if isinstance(code_final[-1], ast.With):
            insert_returns(code_final[-1].body)

    insert_returns()

    exec(compile(code_parsed, filename="<ast>", mode="exec"), env)
    return repr(await eval(f"nice_eval()", env))


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
