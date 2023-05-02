from __future__ import annotations

import io

from os import PathLike
from asyncio import sleep, get_event_loop, AbstractEventLoop
from typing import Dict, Optional, List, Callable, Union
from logging import Logger, StreamHandler, basicConfig, getLogger, WARNING

from .item import Item, BSGItem
from .requester import HTTPRequester
from .utils import MISSING
from .errors import InvalidArgument, NotFound


basicConfig(level=WARNING)
log: Logger = getLogger('client')
stream: StreamHandler = StreamHandler()
stream.setLevel(level=WARNING)
# stream.setFormatter()
log.addHandler(stream)

__all__ = (
    'Client',
)


class Client:

    def __init__(
        self,
        *,
        token: str,
        loop: Optional[AbstractEventLoop] = None,
        refresh_rate: Optional[float] = 60.0,
        refresh_bsg_items: bool = False,
    ):
        self.loop: AbstractEventLoop = get_event_loop() if loop is None else loop
        self.__requester: HTTPRequester = HTTPRequester(token=token, loop=loop)
        self.token: str = token

        if refresh_rate:
            self.loop.create_task(self.__refresh_event(refresh_rate, refresh_bsg_items))

        self._clear()

    def _clear(self) -> None:
        self._items: Dict[str, Item] = {}
        self._bsg_items: Dict[str, BSGItem] = {}

    def get_item(
        self,
        name: str = MISSING,
        *,
        uid: str = MISSING,
        bsg_id: str = MISSING,
    ) -> Optional[Item]:

        if name is not MISSING:
            return self._items.get(name)

        if uid is not MISSING:
            data = {
                item.uid: item
                for item in self._items.values()
            }
            return data.get(uid)

        if bsg_id is not MISSING:
            data = {
                item.bsg_id: item
                for item in self._items.values()
            }
            return data.get(bsg_id)

        raise InvalidArgument('One argument must be entered.')

    def find_items(
        self,
        item_name: Optional[str] = None,
        *,
        check: Callable[[Item], bool] = MISSING
    ) -> List[Item]:

        if check is MISSING:

            def check(i: Item):
                return item_name.lower() in i.name.lower() or item_name.lower() in i.short_name.lower()

        result = [
            item for item in self.items if check(item)
        ]

        return result

    async def fetch_item(self, item_name: str, lang: Optional[str] = MISSING) -> Item:
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

        data = await self.__requester.get_items(item_name, lang=lang)

        if not data:
            raise NotFound(f'Item with name {item_name} not found.')

        return Item(payload=data[0])

    async def fetch_items(self, item_name: str, lang: Optional[str] = MISSING) -> List[Item]:
        """|coro|
        Gets a :class:`.Item`.

        Returns
        -------
        :class:`.Item`
            The items you requested.
        """

        data = await self.__requester.get_items(item_name, lang=lang)

        if not data:
            raise NotFound(f'Item with name {item_name} not found.')

        return [Item(payload=d) for d in data]

    async def fetch_all_items(
        self,
        sort: str = MISSING,
        sort_direction: str = MISSING,
        tags: List[str] = MISSING,
    ) -> List[Item]:
        data = await self.__requester.get_all_items(sort=sort, sort_direction=sort_direction, tags=tags)

        return [Item(payload=d) for d in data]

    async def save_items(
        self,
        fp: Union[io.BufferedIOBase, PathLike],
        *,
        seek_begin: bool = True
    ) -> int:

        data = await self.__requester.save_json()

        if isinstance(fp, io.BufferedIOBase):
            written = fp.write(data)

            if seek_begin is True:
                fp.seek(0)

            return written

        with open(fp, 'wb') as f:
            return f.write(data)

    def get_bsg_item(self, item_id: str) -> BSGItem:
        return self._bsg_items.get(item_id)

    async def fetch_bsg_all_items(self) -> List[BSGItem]:
        data = await self.__requester.get_bsg_all_items()
        return [BSGItem(payload=d) for d in data]

    def start(self, *, load_bsg_items: bool = False) -> None:
        self.loop.run_until_complete(self.load_data(bsg_items=load_bsg_items))

    async def load_data(self, *, bsg_items: bool = True) -> None:
        data = await self.__requester.get_all_items()

        if not data:
            return

        self._clear()

        for payload in data:
            item = Item(payload=payload)
            self._items[item.name] = item

        if bsg_items is True:
            data = await self.__requester.get_bsg_all_items()

            for payload in data:
                item = BSGItem(payload=payload)
                self._bsg_items[item.id] = item

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.__requester.close()

    @property
    def items(self) -> List[Item]:
        return list(self._items.values())

    async def __refresh_event(self, refresh_rate: float, bsg_items: bool) -> None:

        if refresh_rate <= 0:
            return

        while not self.loop.is_closed():
            await sleep(refresh_rate)
            await self.load_data(bsg_items=bsg_items)
