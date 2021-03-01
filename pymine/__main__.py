import concurrent.futures
import asyncio
import sys
import os

if not sys.implementation.version[:3] >= (3, 7, 9):  # Ensure user is on correct version of Python
    print("You are not on a supported version of Python. Please update to version 3.7.9 or later.")
    exit(1)

# try:
#     import uvloop
#
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
# except BaseException:
#     uvloop = None

# ensure the pymine modules are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ensure the current working directory is correct
os.chdir(os.path.join(os.path.dirname(__file__), ".."))

from pymine.api.errors import ServerBindingError
from pymine.api.console import Console
import pymine.server


async def main():
    console = Console()

    asyncio.get_event_loop().set_exception_handler(console.task_exception_handler)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        server = pymine.server.Server(console, executor)
        pymine.server.server = server

        try:
            await server.start()
        except ServerBindingError as e:
            console.error(e.msg)
        except BaseException as e:
            console.critical(console.f_traceback(e))

        try:
            await server.stop()
        except BaseException as e:
            console.critical(console.f_traceback(e))

    exit(0)


if __name__ == "__main__":
    asyncio.run(main())
