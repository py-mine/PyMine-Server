# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from prompt_toolkit import print_formatted_text, PromptSession, ANSI
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.application.current import get_app
from prompt_toolkit.patch_stdout import StdoutProxy
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.output import create_output
from prompt_toolkit.history import FileHistory
from prompt_toolkit.enums import EditingMode
import traceback
import logging
import inspect
import asyncio
import time
import sys
import os
import io

import pymine.api.console_log_formatter

if os.name == "nt":
    import colorama

    colorama.init()


class Console:
    """Custom logging + input implementation."""

    def __init__(self, debug: bool = True) -> None:
        self.debug_ = debug
        self.prompt = "> "
        self.bindings = KeyBindings()

        self.stdout = StdoutProxy(sleep_between_writes=0.5)
        self.out = create_output(self.stdout)
        self.alt_out = io.IOBase()
        self.alt_out.write = self.out.write_raw
        self.alt_out.flush = self.out.flush
        self.log_handler = logging.StreamHandler(self.alt_out)

        log_format = "[{asctime} {levelname}:'{name}']: {message}"
        time_format = "%Y-%m-%d %H:%M:%S"

        self.log_formatter = pymine.api.console_log_formatter.CustomFormatter(
            fmt=log_format,
            datefmt=time_format,
        )

        self.log_handler.setFormatter(self.log_formatter)
        self.logger = logging.getLogger()
        self.logger.addHandler(self.log_handler)

        if self.debug_:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.debug("Started Logger")

        self.ses = PromptSession(
            history=FileHistory("./.pmhist"),
            auto_suggest=AutoSuggestFromHistory(),
            key_bindings=self.bindings,
            mouse_support=True,
            output=self.out,
        )

    def set_prompt(self, prompt: str = None):
        if prompt is not None:
            self.prompt = ANSI(prompt)

    async def fetch_input(self):
        return await self.ses.prompt_async(self.prompt)

    def write(self, text: str):
        self.out.write_raw(text)
        self.out.flush()

    def get_logger(self):
        curframe = inspect.currentframe().f_back.f_back
        logger = logging.getLogger(inspect.getmodule(curframe).__name__)
        return logger

    def build_msg(self, message):
        return " ".join([str(m) for m in message])

    def debug(self, *message):
        self.get_logger().debug(self.build_msg(message))

    def info(self, *message):
        self.get_logger().info(self.build_msg(message))

    def warn(self, *message):
        self.get_logger().warning(self.build_msg(message))

    def error(self, *message):
        self.get_logger().error(self.build_msg(message))

    def critical(self, *message):
        self.get_logger().critical(self.build_msg(message))

    @staticmethod
    def f_traceback(e: BaseException):
        return "\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__, 200)).rstrip("\n")

    def task_exception_handler(self, loop, ctx):
        if ctx.get("exception"):
            self.error(self.f_traceback(ctx["exception"]))
        else:
            self.error(ctx["message"])


if __name__ == "__main__":  # Used to test colors
    console = Console()

    console.debug("This is a", "debug message")
    console.info("This is an", "info message")
    console.warn("This is a", "warning message")
    console.error("This is an", "error message")
    console.critical("This is a", "critical error message")
