import logging
from typing import Optional
from colorama import Fore, Back, Style
import colorama


class CustomFormatter(logging.Formatter):

    log_levels = {
        logging.NOTSET: {"name": "logging.NOTSET", "styles": [Fore.WHITE]},
        logging.DEBUG: {"name": "logging.DEBUG", "styles": [Fore.WHITE, Style.DIM]},
        logging.INFO: {"name": "logging.INFO", "styles": [Fore.BLUE]},
        logging.WARNING: {"name": "logging.WARNING", "styles": [Fore.YELLOW]},
        logging.ERROR: {"name": "logging.ERROR", "styles": [Fore.RED]},
        logging.CRITICAL: {"name": "logging.CRITICAL", "styles": [Fore.WHITE, Back.RED]},
    }

    def __init__(
        self,
        fmt: Optional[str] = "[{asctime} {levelname}:'{name}']: {message}",
        datefmt: Optional[str] = "%Y-%m-%d %H:%M:%S",
        style: str = "{",
        validate: bool = True,
    ) -> None:
        self.fmt = fmt
        self.datefmt = datefmt

        super().__init__(fmt=fmt, datefmt=datefmt, style=style, validate=validate)

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno in self.log_levels:
            level = self.log_levels[record.levelno]
        else:
            level = self.log_levels[logging.NOTSET]

        prefix = "".join(level["styles"])
        record.msg = prefix + record.msg + Style.RESET_ALL
        return super().format(record)
