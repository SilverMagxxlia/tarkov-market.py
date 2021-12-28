from __future__ import annotations

import io

from os import PathLike
from asyncio import get_event_loop, Event, AbstractEventLoop
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Dict, Optional, List, Callable, Union
from logging import Logger, StreamHandler, basicConfig, getLogger, WARNING

from .item import Item, BSGItem
from .http import HTTPClient
from .utils import MISSING
from .errors import InvalidArgument


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
        refresh_rate: Optional[float] = 59.0,
    ):
        self.loop: AbstractEventLoop = get_event_loop() if loop is None else loop
        self.http: HTTPClient = HTTPClient(token=token, loop=loop)
        self.token: str = token

        if refresh_rate:
            sched = AsyncIOScheduler()
            sched.add_job(self.synchronize, 'cron', minute=refresh_rate)
            sched.start()

        self._ready: Event = Event()
        self._closed: bool = False
        self._clear()

    def _clear(self) -> None:
        self._items: Dict[str, Item] = {}
        self._bsg_items: Dict[str, BSGItem] = {}
        self._ready.clear()

    def _handle_ready(self) -> None:
        self._ready.set()

    def is_ready(self) -> bool:
        return self._ready.is_set()

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

        data = await self.http.get_item_by_name(item_name, lang=lang)

        return Item(http=self.http, payload=data[0])

    async def fetch_items(self, item_name: str, lang: Optional[str] = None) -> List[Item]:
        """|coro|
        Gets a :class:`.Item`.

        Returns
        -------
        :class:`.Item`
            The items you requested.
        """

        data = await self.http.get_item_by_name(item_name, lang=lang)

        return [Item(http=self.http, payload=d) for d in data]

    async def save_items(
            self,
            fp: Union[io.BufferedIOBase, PathLike],
            *,
            seek_begin: bool = True
    ) -> int:

        data = await self.http.save_json()

        if isinstance(fp, io.BufferedIOBase):
            written = fp.write(data)

            if seek_begin is True:
                fp.seek(0)

            return written

        with open(fp, 'wb') as f:
            return f.write(data)

    async def wait_until_ready(self) -> None:
        await self._ready.wait()

    def start(self) -> None:
        self.loop.run_until_complete(self.ready())

    async def ready(self) -> None:

        ready: bool = False

        try:
            await self.synchronize()
            ready = True

        except Exception as error:
            log.critical(f'Fail to ready client: {error}')

        finally:

            if ready is True:
                log.debug('Client is now ready.')

    async def synchronize(self) -> None:
        self._clear()

        data = await self.http.get_all_items()

        for payload in data:
            item = Item(http=self.http, payload=payload)
            self._items[item.name] = item

        data = await self.http.get_all_bsg_items()

        for payload in data.values():
            item = BSGItem(payload=payload)
            self._bsg_items[item.id] = item

    @property
    def items(self) -> List[Item]:
        return list(self._items.values())
