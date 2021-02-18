import importlib
import asyncio
import os

from pymine.util.stop import stop

from pymine.api.parsers import parsers


class CommandHandler:
    def __init__(self, server):
        self.server = server
        self.console = server.console
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
                self.console.error(self.console.f_traceback(e))
        elif cmd != "":
            self.console.warn(f"Invalid/unknown command: {repr(cmd)}")

    async def handle_console(self):
        eoferr = False

        try:
            command = ""

            while True:
                inp = "".join([chr(c) for c in self.console.get_input(raw_keys=True)[1]])
                self.console.screen.write(inp)
                command += inp

                if "\n" in command:
                    await self.server_command(command[:-1])

                    if command.startswith("stop"):
                        break

                    command = ""

                await asyncio.sleep(0.001)
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        except EOFError:
            eoferr = True
        except BaseException as e:
            self.console.error(self.console.f_traceback(e))

        if eoferr:
            await stop(self.server)
