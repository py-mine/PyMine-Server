import traceback
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


class Logger:
    """Custom logging implementation.

    :param bool debug: Whether to show debug messages or not.
    :ivar type debug_: The value of the debug parameter.
    """

    def __init__(self, debug: bool = True) -> None:
        self.debug_ = debug

    def debug(self, *message):
        if self.debug_:
            message = " ".join([str(m) for m in message])
            print(f"{WHITE}[{f_time()} {GREY}DEBUG{WHITE}]: {GREY}{message}{END}")

    def info(self, *message):
        message = " ".join([str(m) for m in message])
        print(f"{BRIGHT}{WHITE}[{f_time()} {BLUE}INFO{WHITE}]: {message}{END}")

    def warn(self, *message):
        message = " ".join([str(m) for m in message])
        print(f"{BRIGHT}{WHITE}[{f_time()} {YELLOW}WARNING{WHITE}]: {YELLOW}{message}{END}")

    warning = warn  # for slight compatibility with the built-in logging module

    def error(self, *message):
        message = " ".join([str(m) for m in message])
        print(f"{BRIGHT}{WHITE}[{f_time()} {RED}ERROR{WHITE}]: {RED}{message}{END}")

    def critical(self, *message):
        message = " ".join([str(m) for m in message])
        print(f"{BRIGHT}{WHITE}{BG_RED}[{f_time()} CRITICAL]: {message}{END}")

    @staticmethod
    def f_traceback(e: BaseException):
        return "\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__, 200)).rstrip("\n")


def task_exception_handler(loop, ctx):
    if ctx["exception"]:
        print(f'{BRIGHT}{WHITE}[{f_time()} {RED}ERROR{WHITE}]: {RED}{Logger.f_traceback(ctx["exception"])}{END}')
    else:
        print(f'{BRIGHT}{WHITE}[{f_time()} {RED}ERROR{WHITE}]: {RED}{ctx["message"]}{END}')


if __name__ == "__main__":  # Used to test colors
    logger = Logger()

    logger.debug("This is a", "debug message")
    logger.info("This is an", "info message")
    logger.warn("This is a", "warning message")
    logger.error("This is an", "error message")
    logger.critical("This is a", "critical error message")
