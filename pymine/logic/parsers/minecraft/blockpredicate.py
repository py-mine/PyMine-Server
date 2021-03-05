from pymine.data.block_states import BLOCK_STATES
from pymine.api.errors import ParsingError
from pymine.api.abc import AbstractParser

class BlockPredicate(AbstractParser):
    def __init__(self) -> None:
        pass

    def parse(self, s: str, p:[Player, None]) -> tuple:
        section = s.split()[0]
        try:
            return len(section), BLOCK_STATES[section]
        except BaseException:
            pass
        raise ParsingError
