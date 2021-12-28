import asyncio
import tarkov_market

from typing import List

loop = asyncio.get_event_loop()
market = tarkov_market.Client(token='INSERT YOUR API KEY.', loop=loop)


async def main():
    # fetch the latest data from tarkov-market.
    # there is a limit of 300 requests per minute to fetch.

    # return the first data item from the request result.
    item: tarkov_market.Item = await market.fetch_item('TerraGroup Labs keycard (Red)')

    # return the items from the request results.
    items: List[tarkov_market.Item] = await market.fetch_items('keycard')

    return item

if __name__ == '__main__':
    loop.run_until_complete(main())
    loop.close()
