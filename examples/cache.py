import asyncio
import tarkov_market

from typing import List, Optional
from tarkov_market import Item

TOKEN: str = 'YOUR API KEY'
market = tarkov_market.Client(token=TOKEN)


async def main() -> None:
    # return the item in a pre-cached dictionary.
    # The get method must match all names.
    item: Optional[Item] = market.get_item('TerraGroup Labs keycard (Red)')

    if item is not None:
        print(item.name, item.price)

    # You can also get item with bsg id or uid.
    # All items with the key name will be returned.
    item: Optional[Item] = market.get_item(bsg_id='59faff1d86f7746c51718c9c')
    print(item.name, item.price)

    # Use the find_items function to search for items.
    items: List[Item] = market.find_items('key')

    for item in items:
        print(item.name, item.price)


if __name__ == '__main__':
    # functions such as get, find_items above can only be done using the start function above.
    # This function must be called first before use functions such as get, find_items.
    market.start(load_bsg_items=False)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
