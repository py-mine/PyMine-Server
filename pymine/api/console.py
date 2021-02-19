from prompt_toolkit import PromptSession, ANSI, print_formatted_text
from prompt_toolkit.patch_stdout import StdoutProxy
from prompt_toolkit.output import create_output
import traceback
import asyncio
import time
import os

if os.name == "nt":
    import colorama

    colorama.init()

f_time = lambda: time.strftime("%x %H:%M:%S")

BRIGHT = "\x1b[1m"
END = "\x1b[0m"
WHITE = "\x1b[97m"
GREY = "\x1b[37m"
BLUE = "\x1b[34m"
YELLOW = "\x1b[33m"
RED = "\x1b[91m"
BG_RED = "\x1b[41;1m"


class Console:
    """Custom logging + input implementation."""

    def __init__(self, debug: bool = True) -> None:
        self.debug_ = debug

        self.stdout = StdoutProxy()
        self.out = create_output(self.stdout)
        self.ses = PromptSession(output=self.out)

    async def fetch_input(self):
        return await self.ses.prompt_async("> ")

    def write(self, text: str):
        self.out.write_raw(text + "\n")
        self.out.flush()

    def debug(self, *message):
        if self.debug_:
            message = " ".join([str(m) for m in message])
            self.write(f"{WHITE}[{f_time()} {GREY}DEBUG{WHITE}]: {GREY}{message}{END}")

    def info(self, *message):
        message = " ".join([str(m) for m in message])
        self.write(f"{BRIGHT}{WHITE}[{f_time()} {BLUE}INFO{WHITE}]: {message}{END}")

    def warn(self, *message):
        message = " ".join([str(m) for m in message])
        self.write(f"{BRIGHT}{WHITE}[{f_time()} {YELLOW}WARNING{WHITE}]: {YELLOW}{message}{END}")

    def error(self, *message):
        message = " ".join([str(m) for m in message])
        self.write(f"{BRIGHT}{WHITE}[{f_time()} {RED}ERROR{WHITE}]: {RED}{message}{END}")

    def critical(self, *message):
        message = " ".join([str(m) for m in message])
        self.write(f"{BRIGHT}{WHITE}{BG_RED}[{f_time()} CRITICAL]: {message}{END}")

    @staticmethod
    def f_traceback(e: BaseException):
        return "\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__, 200)).rstrip("\n")

    def task_exception_handler(self, loop, ctx):
        if ctx["exception"]:
            print(f'{BRIGHT}{WHITE}[{f_time()} {RED}ERROR{WHITE}]: {RED}{self.f_traceback(ctx["exception"])}{END}')
        else:
            print(f'{BRIGHT}{WHITE}[{f_time()} {RED}ERROR{WHITE}]: {RED}{ctx["message"]}{END}')


if __name__ == "__main__":  # Used to test colors
    console = Console()

    console.debug("This is a", "debug message")
    console.info("This is an", "info message")
    console.warn("This is a", "warning message")
    console.error("This is an", "error message")
    console.critical("This is a", "critical error message")
