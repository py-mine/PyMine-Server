import asyncio_dgram
import asyncio

from src.util.share import share


async def ping_lan():
    while True:
        try:
            stream = await asyncio.wait_for(asyncio_dgram.connect(('224.0.2.60', 4445)), .5)

            await stream.send(
                f'[MOTD]{share["conf"]["motd"]}[/MOTD]' \
                f'[AD]{share["conf"]["server_port"]}[/AD]'.encode('utf-8')
            )

            stream.close()
        except Exception:
            pass

        await asyncio.sleep(1.5)
