import aioconsole
import asyncio

from src.util.share import share

registered_commands = {}


def command(name: str):
    if name in registered_commands:
        raise Exception('Command name is already in use.')

    if ' ' in name:
        raise Exception('Command name may not contain spaces.')

    def command_deco(func: 'function'):
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

            reg_cmd = registered_commands.get(cmd)

            if reg_cmd is not None:
                await reg_cmd('server', args)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    except Exception as e:
        print(e)


@command(name='stop')
async def stop_server(uuid: str, cmd: str):
    share['server'].stop()
