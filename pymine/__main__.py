import asyncio
import sys
import os

# ensure the pymine modules are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymine.util.logging import Logger, task_exception_handler
import pymine.server

if __name__ == "__main__":
    logger = Logger()  # debug status will be set later after config is loaded

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(task_exception_handler)

    server = pymine.server.Server(logger)
    pymine.server.server = server

    try:
        loop.run_until_complete(server.start())
    except asyncio.CancelledError:
        pass
    except BaseException as e:
        logger.critical(logger.f_traceback(e))

    try:
        loop.run_until_complete(server.stop())
    except BaseException as e:
        logger.critical(logger.f_traceback(e))

    loop.stop()
    loop.close()
