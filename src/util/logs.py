import logging


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = '\x1b[38;21m'
    yellow = '\x1b[33;1m'
    red = '\x1b[31;21m'
    bold_red = '\x1b[31;1m'
    blue = '\x1b[34m'
    green = '\x1b[32m'
    bg_bright_red = '\x1b[41;1m'
    reset = '\x1b[0m'
    everythings_fine_format = '%(levelname)s' + reset + \
        ': %(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)'
    oh_no_format = '%(levelname)s: %(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)'

    FORMATS = {
        logging.DEBUG: grey + everythings_fine_format + reset,
        logging.INFO: blue + everythings_fine_format + reset,
        logging.WARNING: yellow + oh_no_format + reset,
        logging.ERROR: bold_red + oh_no_format + reset,
        logging.CRITICAL: bg_bright_red + oh_no_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


if __name__ == '__main__':
    logger = logging.getLogger('testing')
    logger.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
