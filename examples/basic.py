import asyncio
import tarkov_market

from typing import List

loop = asyncio.get_event_loop()
market = tarkov_market.Client(token='INSERT YOUR API KEY.', refresh_rate=None)


async def main():
    # Find Item and return Items from pre-loaded Item List. It's Unlimited.
    items: List[tarkov_market.Item] = market.find_items('keycard')

    # Get Item by name. Can get it through uid and bsg_id.
    item: tarkov_market.Item
    item = market.get_item('Tactical glasses')
    item = market.get_item(bsg_id='BSG_ID')
    item = market.get_item(uid='UID')

if __name__ == '__main__':
    market.start()
    loop.run_until_complete(main())
    loop.close()
