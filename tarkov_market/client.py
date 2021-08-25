import aiohttp
import asyncio

from typing import Any, Dict, Optional, List

from .item import Item
from .http import HTTPClient

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
        self.http = HTTPClient(connector, token=token)

        self._closed: bool = False
        self.clear()

    def clear(self):
        self._items: Dict[str, Item] = {}

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

        return Item(data[0])

    async def fetch_items(self, item_name: str, lang: Optional[str] = None) -> List[Item]:

        async with self.http as http:
            data = http.get_item_by_name(item_name, lang=lang)

        return [Item(d) for d in data]

    async def close(self) -> None:

        if self._closed:
            return

        self._closed = True
        await self.http.close()

    async def setup(self) -> None:

        async with self.http as session:
            await session.recreate()

            data = await session.get_all_items()

            for payload in data:
                item = Item(payload)
                self._items[item.name] = item

    async def __aenter__(self):
        return self.http.__aenter__()

    async def __aexit__(self, *args):
        return self.http.__aexit__(*args)
