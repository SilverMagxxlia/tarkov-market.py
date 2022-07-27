import asyncio
import tarkov_market

from typing import List
from tarkov_market import Item

TOKEN: str = 'YOUR API KEY'
market = tarkov_market.Client(token=TOKEN, refresh_rate=None)


async def main() -> None:
    # return only one of the search results
    item: Item = await market.fetch_item('TerraGroup Labs keycard (Red)')

    print(item.name, item.price)

    # return all search results
    items: List[Item] = await market.fetch_items('key')

    for item in items:
        print(item.name, item.price)

    '''
    The fetch functions has a limit of 300 requests per minute because it communicates directly with the API.
    If you have a large number of requests, check the example in the link below.
    
    cache example: https://github.com/Hostagen/tarkov-market.py/blob/master/examples/cache.py
    
    Unrestricted by pre-loading and caching data once.
    '''


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
