import asyncio
import bitblock
import tracemalloc

tracemalloc.start()


async def main():
    bb = bitblock.BitBlock("user", "localBTC!", "http://127.0.0.1:8332")

asyncio.run(main(), debug=True)