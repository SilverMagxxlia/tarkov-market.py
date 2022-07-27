Tarkov-Market.py
=========================

.. image:: https://img.shields.io/pypi/v/tarkov-market.py?color=ffd242&logo=pypi&logoColor=ffffff&style=for-the-badge
    :alt: PyPI
    :target: https://pypi.org/project/tarkov-market.py/
.. image:: https://img.shields.io/github/v/release/hostagen/tarkov-market.py?color=007ec6&include_prereleases&logo=github&style=for-the-badge
    :alt: GitHub release (latest by date including pre-releases)
.. image:: https://img.shields.io/badge/Tarkov--Market-Provides%20API-9a8866?style=for-the-badge&logo=appveyor&logoColor=ffffff
    :target: https://tarkov-market.com/

async API wrapper for Tarkov Market written in Python. It is designed to reverse `discord.py <https://github.com/Rapptz/discord.py>`_ as a base.

Installing
----------
**Python 3.8 or higher is required**

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U tarkov-market.py

    # Windows
    py -3 -m pip install -U tarkov-market.py

Quick Examples
---------------

Basic use with use client
'''''''''''''''''''''''''''

.. code:: py

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

Simple to use without client declaration
''''''''''''''''''''''''''''''''''''''''''

.. code:: py

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

More Examples
--------------
https://github.com/Hostagen/tarkov-market.py/tree/master/examples

Update Logs
-------------
`Check here for releases <https://github.com/Hostagen/tarkov-market.py/releases>`_
