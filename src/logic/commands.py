from src.util.aioinput import aioinput


async def handle_commands():
    try:
        while True:
            print(await aioinput(''))
    except KeyboardInterrupt:
        pass
