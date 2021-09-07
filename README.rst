.. image:: https://user-images.githubusercontent.com/68284806/130361774-5fe5866f-d61b-40a3-afc1-2978ad530f17.png
    :align: center
    :height: 128
    :target: https://github.com/Hostagen/tarkov-market.py
    :alt: PyPI

async API wrapper for Tarkov Market written in Python. It is designed to reverse `discord.py <https://github.com/Rapptz/discord.py>`_ as a base.

`About <About>`_ | `PyPI <https://pypi.org/project/tarkov-market.py/>`_

About
-----
What is Tarkov-Market.py?
=======================

- Tarkov-Market.py is Modern Python API using `async` and `await`.

Installing
=======
**Python 3.8 or higher is required**

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U tarkov-market.py

    # Windows
    py -3 -m pip install -U tarkov-market.py

Quick Example
------------

.. code:: py

    import asyncio
    import tarkov_market

    from typing import List

    market = tarkov_market.Client(token='INSERT YOUR API KEY.')


    async def main():
        # Must run setup once before use.
        await market.setup()

        # Find Item and return Items from pre-loaded Item List. It's Unlimited.
        item: List[tarkov_market.Item] = market.find_items('TerraGroup Labs keycard (Red)')

        return item

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
