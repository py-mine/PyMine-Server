from src.logic.commands import command
from src.util.share import share


@command(name='stop', node='minecraft.cmd.stop')
def stop_server(uuid: str, args: str):
    share['server'].close()
