from src.logic.commands import command
from src.util.share import share


@command(name='stop')
def stop_server(uuid: str, args: list):
    share['server'].close()
