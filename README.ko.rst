.. image:: https://user-images.githubusercontent.com/68284806/130361774-5fe5866f-d61b-40a3-afc1-2978ad530f17.png
    :align: center
    :height: 128
    :target: https://github.com/Hostagen/tarkov-market.py
    :alt: PyPI

Python으로 이루어진 Tarkov Market API 비동기 라이브러리입니다.

.. class:: center

    `PyPI <https://pypi.org/project/tarkov-market.py/>`_

Tarkov-Market.py는 무엇입니까?
-------------------------

- Tarkov-Market.py는 간단한 `async`와 `await`를 사용한 Python API입니다.

설치
----------
**Python 3.8 이상의 버전이 요구됩니다.**

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U tarkov-market.py

    # Windows
    py -3 -m pip install -U tarkov-market.py

빠른 예시
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

Fetch 예시
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
