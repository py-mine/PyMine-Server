import aioconsole
import importlib
import traceback
import asyncio
import os

from src.util.share import share, logger

registered_commands = {}


def load_commands():  # only loads commands inside cmds folder, not subfolders
    for file in os.listdir('src/logic/cmds'):
        if file.endswith('.py'):
            importlib.import_module(f'src.logic.cmds.{file[:-3]}')


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

            print(cmd_func)

            try:
                if cmd_func is not None:
                    if asyncio.iscoroutinefunction(cmd_func):
                        await cmd_func('server', args)
                    else:
                        cmd_func('server', args)
            except Exception as e:
                logger.error(''.join(traceback.format_exception(type(e), e, e.__traceback__, 4)))
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
