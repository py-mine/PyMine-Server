import aioconsole
import asyncio

from src.util.share import share

registered_commands = {}

# Example command
# @command(name='somecmd')
# async def some_command(uuid: str, text: str) -> none:
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
        cmd = await aioconsole.ainput('>')
        reg_cmd = registered_commands.get(cmd.split(' ')[0])

        if reg_cmd is not None:
            await reg_cmd('server', cmd)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
