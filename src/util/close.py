from src.util.share import share


async def close_server():
    share['server'].close()
    await share['server'].wait_closed()
