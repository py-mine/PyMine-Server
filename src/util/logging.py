import time
import os

if os.name == 'nt':
    import colorama
    colorama.init()

nice_time = (lambda: time.strftime('%x %H:%M:%S'))

RESET = '\x1b[0m'
WHITE = '\x1b[97m'
GREY = '\x1b[37m'
BLUE = '\x1b[34m'
YELLOW = '\x1b[33m'
RED = '\x1b[91m'
BG_RED = '\x1b[41;1m'


class Logger:
    def __init__(self, debug: bool = True) -> None:
        self.debug = debug

    def debug(self, *message):
        if self.debug:
            message = ' '.join(str(m) for m in message)
            print(f'{WHITE}[{nice_time()} {GREY}DEBUG{WHITE}]: {GREY}{message}{RESET}')

    def info(self, *message):
        message = ' '.join(str(m) for m in message)
        print(f'{WHITE}[{nice_time()} {BLUE}INFO{WHITE}]: {message}{RESET}')

    def warn(self, *message):
        message = ' '.join(str(m) for m in message)
        print(f'{WHITE}[{nice_time()} {YELLOW}WARNING{WHITE}]: {YELLOW}{message}{RESET}')

    def error(self, *message):
        message = ' '.join(str(m) for m in message)
        print(f'{WHITE}[{nice_time()} {RED}ERROR{WHITE}]: {RED}{message}{RESET}')

    def critical(self, *message):
        message = ' '.join(str(m) for m in message)
        print(f'{WHITE}{BG_RED}[{nice_time()} CRITICAL ERROR]: {message}{RESET}')
