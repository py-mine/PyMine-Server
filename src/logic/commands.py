from src.util.aioinput import aioinput


async def handle_commands():
    while True:
        print(await aioinput('>'))
