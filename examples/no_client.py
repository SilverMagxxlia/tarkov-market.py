import asyncio

from typing import List
from tarkov_market import Client as TVMClient, Item

TOKEN: str = 'YOUR API KEY'


async def main():
    async with TVMClient(token=TOKEN) as api:
        item: Item = await api.fetch_item('TerraGroup Labs keycard (Red)')
        print(item.name, item.price)

        items: List[Item] = await api.fetch_items('key')

        for item in items:
            print(item.name, item.price)

    # When you exit the `async with` syntax, aiohttp.ClientSession is automatically and securely terminated.
    # When you use the `async with` with again, a new aiohttp.ClientSession is created again.

    async with TVMClient(token=TOKEN) as api:
        ...


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
