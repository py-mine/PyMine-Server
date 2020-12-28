import aioconsole
import asyncio

from src.util.share import share

registered_commands = {}

# Example command
# @command(name='somecmd')
# async def some_command(uuid: str, args: list) -> none:
#     pass


def command(name: str):
    if name in registered_commands:
        raise Exception('Command name is already in use.')

    if ' ' in name:
        raise Exception('Command name may not contain spaces.')

    async def command_deco(func: 'function'):
        if not asyncio.iscoroutine(func):
            raise Exception('Commands must be coroutines.')

        registered_commands[name] = func
        return func

    return command_deco


async def handle_commands():
    try:
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
