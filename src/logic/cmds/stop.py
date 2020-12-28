from src.logic.commands import command
from src.util.share import share


@command(name='stop')
async def stop_server(uuid: str, args: list):
    share['server'].close()
