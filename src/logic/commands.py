import asyncio

from src.util.close import close_server
from src.util.aioinput import aioinput


async def handle_command(cmd: str):
    if cmd == 'stop':
        await close_server()
        return False

    return True


async def handle_commands(server, cmd_task):
    run = True

    try:
        while run:
            run = await handle_command(await aioinput(''))
    except KeyboardInterrupt:
        pass
