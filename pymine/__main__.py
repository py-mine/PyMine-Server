import asyncio
import sys
import os

# ensure the pymine modules are accessible
sys.path.append(os.path.join(os.getcwd(), os.path.split(__file__)[0]))

from pymine.util.logging import Logger, task_exception_handler
from pymine.server import Server

if __name__ == "__main__":
    logger = Logger()  # debug status will be set later after config is loaded

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(task_exception_handler)

    server = Server(logger)

    try:
        loop.run_until_complete(server.start())
    except BaseException as e:
        logger.critical(logger.f_traceback(e))

    try:
        loop.run_until_complete(server.stop())
    except BaseException as e:
        logger.critical(logger.f_traceback(e))

    loop.stop()
    loop.close()
