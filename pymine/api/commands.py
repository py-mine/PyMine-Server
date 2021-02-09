import aioconsole
import importlib
import asyncio
import os

from pymine.util.stop import stop


class CommandHandler:
    def __init__(self, server):
        self.server = server
        self.logger = server.logger
        self._commands = {}  # {name: (func, node)}

    # loads default built in commands
    @staticmethod
    def load_commands():  # only loads commands inside cmds folder, not subfolders
        for file in os.listdir("pymine/logic/cmds"):
            if file.endswith(".py"):
                importlib.import_module(f"pymine.logic.cmds.{file[:-3]}")

    def on_command(self, name: str, node: str):
        if name in self._commands:
            raise ValueError("Command name is already in use.")

        if " " in name:
            raise ValueError("Command name may not contain spaces.")

        def deco(func):
            if not asyncio.iscoroutinefunction(func):
                raise ValueError("Decorated object must be a coroutine function.")

            self._commands[name] = func, node
            return func

        return deco

    async def server_command(self, in_text: str):
        in_split = in_text.split(" ")
        cmd = in_split.pop(0)

        args = " ".join(in_split)

        reg_cmd = self._commands.get(cmd)

        if reg_cmd is not None:
            cmd_func = reg_cmd[0]

            try:
                await cmd_func("server", args)
            except BaseException as e:
                self.logger.error(self.logger.f_traceback(e))
        elif cmd != "":
            self.logger.warn(f"Invalid/unknown command: {cmd}")

    async def handle_console(self):
        eoferr = False

        try:
            while True:
                in_text = await aioconsole.ainput(">")

                # In the future, commands *should* be handled async,
                # however, due to the way the console works rn we can't
                # without messing up the output
                # asyncio.create_task(handle_command(in_text))

                await self.server_command(in_text)

                if in_text.startswith("stop"):
                    break
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        except EOFError:
            eoferr = True
        except BaseException as e:
            self.logger.error(self.logger.f_traceback(e))

        if eoferr:
            await stop(self.server)
