from src.logic.commands import command
from src.util.share import logger


@command(name='test_exception')
def test_exception(uuid: str, args: list):
    raise Exception('This is an Exception!')


@command(name='echo')
def echo(uuid: str, args: list):
    logger.info(f'{uuid}: {" ".join(args)}')
