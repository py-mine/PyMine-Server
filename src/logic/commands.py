import asyncio

from src.util.aioinput import aioinput
from src.util.share import share


async def handle_command(cmd: str):
    if cmd == 'stop':
        share['server'].close()
        return False

    return True


async def handle_commands():
    run = True

    try:
        while run:
            run = await handle_command(await aioinput(''))
    except KeyboardInterrupt:
        pass
