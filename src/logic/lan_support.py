import asyncio

from src.util.share import share


async def ping_lan():
    while True:
        try:
            r, w, = await asyncio.wait_for(
                asyncio.open_connection(
                    host='224.0.2.60',
                    port=4445
                ),
                .5
            )

            w.write(f'[MOTD]{share["conf"]["motd"]}[/MOTD][AD]{share["conf"]["server_port"]}[/AD]'.encode('utf-8'))
            await w.drain()
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print(e)

        await asyncio.sleep(1.5)
