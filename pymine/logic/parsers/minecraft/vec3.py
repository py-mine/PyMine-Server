from pymine.api.errors import ParsingError
from pymine.api.abc import AbstractParser
from pymine.types.player import Player

class Vec2(AbstractParser):
    def __init__(self) -> None:
        pass

    def parse(self, s: str, p:[Player, None]) -> tuple:
        a = s.split()[0]
        b = s.split()[1]
        c = s.split()[2]
        used = len(a) + len(b) + len(c) + 2
        if(p!=None):
            a.replace("~", p.x)
            b.replace("~", p.y)
            c.replace("~", p.z)
        try:
            return used, (float(a), float(b), float(c))
        except BaseException:
            pass
        raise ParsingError
