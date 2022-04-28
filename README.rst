.. image:: https://user-images.githubusercontent.com/68284806/130361774-5fe5866f-d61b-40a3-afc1-2978ad530f17.png
    :align: center
    :height: 128
    :target: https://github.com/Hostagen/tarkov-market.py
    :alt: PyPI

async API wrapper for Tarkov Market written in Python. It is designed to reverse `discord.py <https://github.com/Rapptz/discord.py>`_ as a base.

.. class:: center

    `PyPI <https://pypi.org/project/tarkov-market.py/>`_

What is Tarkov-Market.py?
-------------------------

- Tarkov-Market.py is Modern Python API using `async` and `await`.

Installing
----------
**Python 3.8 or higher is required**

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U tarkov-market.py

    # Windows
    py -3 -m pip install -U tarkov-market.py

Quick Example
-------------

.. code:: py

    import asyncio
    import tarkov_market

    from typing import List

    loop = asyncio.get_event_loop()
    market = tarkov_market.Client(token='INSERT YOUR API KEY.', refresh_rate=None)


    async def main() -> None:
        # Find Item and return Items from preloaded Item List. It's Unlimited.
        items: List[tarkov_market.Item] = market.find_items('keycard')

        # Get Item by name. Can get it through uid and bsg_id.
        item: tarkov_market.Item
        item = market.get_item('Tactical glasses')
        item = market.get_item(bsg_id='BSG_ID')
        item = market.get_item(uid='UID')

        print('Item Name: {}'.format(item.name))
        print('Short Name: {}'.format(item.short_name))
        print('Price {}'.format(item.price))

    if __name__ == '__main__':
        market.start()
        loop.run_until_complete(main())
        loop.close()

Fetch Example
~~~~~~~~~~~~~

.. code:: py

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
