from concurrent.futures import ThreadPoolExecutor
import asyncio


async def aioinput(prompt: str = '') -> str:
    with ThreadPoolExecutor() as pool:
        return await asyncio.run_in_executor(pool, (lambda: input(prompt)))
