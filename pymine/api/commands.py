import aioconsole
import importlib
import asyncio
import os

# loads default built in commands
def load_commands():  # only loads commands inside cmds folder, not subfolders
    for file in os.listdir("pymine/logic/cmds"):
        if file.endswith(".py"):
            importlib.import_module(f"pymine.logic.cmds.{file[:-3]}")


async def handle_server_command(in_text: str):
    in_split = in_text.split(" ")
    cmd = in_split.pop(0)

    args = " ".join(in_split)

    reg_cmd = registered_commands.get(cmd)

    if reg_cmd is not None:
        cmd_func = reg_cmd[0]

        try:
            if asyncio.iscoroutinefunction(cmd_func):
                await cmd_func("server", args)
            else:
                cmd_func("server", args)
        except BaseException as e:
            logger.error(logger.f_traceback(e))
    else:
        logger.warn(f"Invalid/unknown command: {cmd}")


async def handle_server_commands():
    try:
        while True:
            in_text = await aioconsole.ainput(">")

            # In the future, commands *should* be handled async,
            # however, due to the way the console works rn we can't
            # without messing up the output
            # asyncio.create_task(handle_command(in_text))

            await handle_server_command(in_text)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    except BaseException as e:
        logger.error(logger.f_traceback(e))
