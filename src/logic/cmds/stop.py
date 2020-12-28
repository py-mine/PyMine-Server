from src.logic.commands import command
from src.util.share import share


@command(name='stop')
async def stop_server(uuid: str, cmd: str):
    share['server'].close()
