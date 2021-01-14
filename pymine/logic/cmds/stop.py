from pymine.logic.commands import on_command
from pymine.util.share import share


@on_command(name='stop', node='minecraft.cmd.stop')
def stop_server(uuid: str, args: str):
    share['server'].close()
