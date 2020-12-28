from src.util.share import share, logger


async def close_server():
    logger.info('closing server...')

    # Close actual asyncio server
    share['server'].close()
    await share['server'].wait_closed()

    logger.info('server closed.')
