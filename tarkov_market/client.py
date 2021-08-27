from __future__ import annotations

import aiohttp
import asyncio

from typing import Any, Dict, Optional, List, Callable, TYPE_CHECKING

from .item import Item, BSGItem
from .http import HTTPClient
from .utils import MISSING

if TYPE_CHECKING:
    from .types.item import BSGItem as BSGItemPayload

__all__ = (
    'Client',
)


class Client:

    def __init__(
        self,
        *,
        token: str,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        **options: Any
    ):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        self.token: str = token

        connector: Optional[aiohttp.BaseConnector] = options.pop('connector', None)
        self.http = HTTPClient(connector, token=token, loop=loop)

        self._closed: bool = False
        self._clear()

    def _clear(self):
        self._items: Dict[str, Item] = {}
        self._bsg_items: Dict[str, BSGItem] = {}

    def _add_bsg_item(self, payload: BSGItemPayload):
        item_id = payload['_id']
        self._bsg_items[item_id] = BSGItem(payload)

    def get_item(self, item_name: str):
        """
        Returns a item with the given name.

        Parameters
        -----------
        item_name: :class:`str`
            The name to search for.

        Returns
        --------
        Optional[:class:`~tarkov_market.Item`]
            The item or `None` if item not found.
        """

        return self._items.get(item_name)

    def find_items(
            self,
            item_name: Optional[str] = None,
            *,
            check: Callable[[Item], bool] = MISSING
    ) -> List[Item]:

        result = []

        if check is MISSING:

            def check(i: Item):

                if item_name.lower() in i.name.lower():
                    return True

                return False

        for item in self.items:

            if not check(item):
                continue

            result.append(item)

        return result

    def get_bsg_item(self, item_id: str) -> BSGItem:
        return self._bsg_items.get(item_id)

    async def fetch_item(self, item_name: str, lang: Optional[str] = None) -> Item:
        """
        Raises
        --------
        :exc:`.NotFound`
            A Item with this Name does not exist.

        Returns
        --------
        :class:`~tarkov_market.Item`
            The Item you requested.
        """

        async with self.http as http:
            data = await http.get_item_by_name(item_name, lang=lang)

        return Item(http=self.http, payload=data[0])

    async def fetch_items(self, item_name: str, lang: Optional[str] = None) -> List[Item]:
        """|coro|
        Gets a :class:`.Item`.

        Returns
        -------
        :class:`.Item`
            The items you requested.
        """

        async with self.http as http:
            data = http.get_item_by_name(item_name, lang=lang)

        return [Item(http=self.http, payload=d) for d in data]

    async def close(self) -> None:

        if self._closed:
            return

        self._closed = True
        await self.http.close()

    async def setup(self) -> None:
        """|coro|

        Setup HTTPClient.
        """

        async with self.http as session:
            await session.recreate()

            data = await session.get_all_items()

            for payload in data:
                item = Item(http=self.http, payload=payload)
                self._items[item.name] = item

            bsg_item = await session.get_all_bsg_items()

            map(self._add_bsg_item, bsg_item.values())

    @property
    def items(self) -> List[Item]:
        return list(self._items.values())

    async def __aenter__(self):
        return self.http.__aenter__()

    async def __aexit__(self, *args):
        return self.http.__aexit__(*args)
