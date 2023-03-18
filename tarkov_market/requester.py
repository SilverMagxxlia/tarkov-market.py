from __future__ import annotations

import json
import aiohttp
import asyncio

from typing import (
    Any,
    ClassVar,
    Coroutine,
    Optional,
    Union,
    Dict,
    List,
    TypeVar,
    TYPE_CHECKING,
)

from urllib.parse import quote as _uriquote

from . import utils
from .errors import LoginFailure

if TYPE_CHECKING:
    from .types.item import Item as ItemPayload, BSGItem as BSGItemPayload
    from .enums import LangType

    T = TypeVar('T')
    BE = TypeVar('BE', bound=BaseException)
    MU = TypeVar('MU', bound='MaybeUnlock')
    Response = Coroutine[Any, Any, T]


async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding='utf-8')

    try:

        if response.headers['content-type'] == 'application/json; charset=utf-8':
            return json.loads(text)

    except KeyError:
        pass

    return text


class Route:
    BASE: ClassVar[str] = 'https://api.tarkov-market.app/api/v1'

    def __init__(self, method: str, path: str, **parameters: Any):
        self.path: str = path
        self.method: str = method

        url = "{}{}".format(self.BASE, path)

        if parameters:
            url = url.format_map({k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})

        self.url = url


class HTTPRequester:

    def __init__(
        self,
        *,
        token: str,
        session: aiohttp.ClientSession = aiohttp.ClientSession(),
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        self._session = session
        self.token: str = token

    async def request(self, route: Route, **kwargs: Any) -> Any:
        method = route.method
        url = route.url

        headers: Dict[str, str] = {
            "x-api-key": self.token,
        }

        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = utils._to_json(kwargs.pop('json'))

        kwargs['headers'] = headers

        async with self._session.request(method, url, **kwargs) as response:
            data = await json_or_text(response)

            if isinstance(data, dict) and data.get('error') is not None:
                reason = data['error']

                if reason == 'Access denied':
                    raise LoginFailure(f'{self.token} is Invalid API KEY.')

                if reason in (
                    'You reach your limit of 300 reqs per minute',
                    'You reach your limit of 5 req per minute'
                ):
                    await asyncio.sleep(60)
                    return await self.request(route, **kwargs)

            if 300 > response.status >= 200:
                return data

    async def close(self) -> None:
        await self._session.close()

    def get_item_by_name(
        self,
        name: str,
        *,
        lang: Optional[Union[LangType, str]] = None
    ) -> Response[List[ItemPayload]]:

        if lang:
            payload: Dict[str, str] = {
                "q": name,
                "lang": lang
            }
            r = Route('POST', '/item', json=payload)

        else:
            r = Route('GET', '/item?q={item_name}', item_name=name)

        return self.request(r)

    def get_item_by_uid(self, uid) -> Response[List[ItemPayload]]:
        r = Route('GET', '/item?uid={uid}', uid=uid)
        return self.request(r)

    def get_all_items(self, sort: str = None, sort_direction: str = None) -> Response[List[ItemPayload]]:
        url = '/items/all'

        if sort:
            url += f'?sort={sort}'

        if sort_direction:
            url += f'&sort_direction={sort_direction}'

        r = Route('GET', url)
        return self.request(r)

    def get_all_item_by_tag(self, tag: str) -> Response[List[ItemPayload]]:
        r = Route('GET', '/items/all?tag={tag}', tag=tag)
        return self.request(r)

    def get_all_bsg_items(self) -> Response[List[BSGItemPayload]]:
        r = Route('GET', '/bsg/items/all')
        return self.request(r)

    def save_json(self):
        r = Route('GET', '/bsg/items/all/download')
        return self.request(r)
