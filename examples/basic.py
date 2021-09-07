import asyncio
import tarkov_market

from typing import List

market = tarkov_market.Client(token='INSERT YOUR API KEY.')


async def main():
    # Must run setup once before use.
    await market.setup()

    # Find Item and return Items from pre-loaded Item List.
    item: List[tarkov_market.Item] = market.find_items('TerraGroup Labs keycard (Red)')

    return item

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
