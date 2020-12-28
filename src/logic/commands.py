import aioconsole
import asyncio

from src.util.share import share

registered_commands = {}


def command(name: str):
    if name in registered_commands:
        raise Exception('Command name is already in use.')

    if ' ' in name:
        raise Exception('Command name may not contain spaces.')

    def command_deco(func):
        registered_commands[name] = func
        return func

    return command_deco


async def handle_commands():
    try:
        while True:
            in_split = (await aioconsole.ainput('>')).split(' ')
            cmd = in_split[0]

            if len(in_split) > 0:
                args = in_split[1:]
            else:
                args = []

            cmd_func = registered_commands.get(cmd)

            if cmd_func is not None:
                if asyncio.iscoroutinefunction(cmd_func):
                    await cmd_func('server', args)
                else:
                    cmd_func('server', args)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass


@command(name='stop')
async def stop_server(uuid: str, cmd: str):
    share['server'].close()
