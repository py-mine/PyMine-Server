import concurrent.futures
import asyncio
import sys
import os

if not sys.implementation.version[:3] >= (3, 7, 9):  # Ensure user is on correct version of Python
    print("You are not on a supported version of Python. Please update to version 3.7.9 or later.")
    exit(1)

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except BaseException:
    uvloop = None

# ensure the pymine modules are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ensure the current working directory is correct
os.chdir(os.path.join(os.path.dirname(__file__), ".."))

from pymine.util.logging import Logger, task_exception_handler
from pymine.api.errors import ServerBindingError
import pymine.server

if __name__ == "__main__":
    logger = Logger()  # debug status will be set later after config is loaded

    if uvloop:
        logger.debug("Using uvloop as the event loop.")

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(task_exception_handler)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        server = pymine.server.Server(logger, executor, bool(uvloop))
        pymine.server.server = server

        try:
            loop.run_until_complete(server.start())
        except (asyncio.CancelledError, KeyboardInterrupt):
            pass
        except ServerBindingError as e:
            logger.error(
                f"An error occurred while attempting to bind {e.server} server to {e.addr}:{e.port}, is that address already in use?"
            )
        except BaseException as e:
            logger.critical(logger.f_traceback(e))

        try:
            loop.run_until_complete(server.stop())
        except BaseException as e:
            logger.critical(logger.f_traceback(e))

    loop.stop()
    loop.close()
