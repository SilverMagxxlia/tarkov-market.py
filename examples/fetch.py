import asyncio
import tarkov_market

from typing import List

market = tarkov_market.Client(token='INSERT YOUR API KEY.')


async def main():
    # Must run setup once before use.
    await market.setup()

    # fetch the latest data from tarkov-market.
    # there is a limit of 300 requests per minute to fetch.

    # return the first data item from the request result.
    item: tarkov_market.Item = await market.fetch_item('TerraGroup Labs keycard (Red)')

    # return the items from the request results.
    items: List[tarkov_market.Item] = await market.fetch_items('keycard')

    return item

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
