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


def command(name: str, node: str):
    if name in registered_commands:
        raise Exception('Command name is already in use.')

    if ' ' in name:
        raise Exception('Command name may not contain spaces.')

    def command_deco(func):
        registered_commands[name] = func, node
        return func

    return command_deco


async def handle_server_command(uuid: str, in_text: str):
    in_split = in_text.split(' ')
    cmd = in_split.pop(0)

    args = ''.join(in_split)

    reg_cmd = registered_commands.get(cmd)

    if reg_cmd is not None:
        cmd_func = reg_cmd[0]

        try:
            if asyncio.iscoroutinefunction(cmd_func):
                await cmd_func(uuid, args)
            else:
                cmd_func(uuid, args)
        except Exception as e:
            logger.error(
                ''.join(traceback.format_exception(type(e), e, e.__traceback__, 4))
            )
    else:
        logger.warn(f'Invalid/unknown command: {cmd}')


async def handle_server_commands():
    try:
        while True:
            in_text = await aioconsole.ainput('>')

            # In the future, commands *should* be handled async,
            # however, due to the way the console works rn we can't
            # without messing up the output
            # asyncio.create_task(handle_command(in_text))

            await handle_server_command('server', in_text)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    except Exception as e:
        print(e, type(e))
