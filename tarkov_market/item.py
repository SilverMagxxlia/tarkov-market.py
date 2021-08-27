from __future__ import annotations
from typing import Literal, TYPE_CHECKING

import datetime

from .traders import Trader

if TYPE_CHECKING:
    from .http import HTTPClient

    from .types.item import (
        Item as ItemPayload,
        BSGItem as BSGItemPayload,
        BSGPrefab as PrefabPayload
    )
    from .types.trader import Trader as TraderPayload

__all__ = ('Item',)


class Item:

    __slots__ = (
        'uid',
        'bsg_id',
        'name',
        'short_name',
        'price',
        'base_price',
        'slots',
        'avg24h_price',
        'avg7days_price',
        '_updated_at',
        'diff24h',
        'diff7days',
        'link',
        'wiki_link',
        'icon_url',
        'image_url',
        '_http',
        '_trader_payload'
    )

    def __init__(self, http: HTTPClient, payload: ItemPayload):
        self._http = http

        self.uid: str = payload['uid']
        self.bsg_id: str = payload['bsgId']
        self.name: str = payload['name']
        self.short_name: str = payload['shortName']
        self.slots: int = payload['slots']
        self.link: str = payload['link']
        self.wiki_link: str = payload['wikiLink']

        self._update(payload)

    @property
    def trader(self) -> Trader:
        return Trader(self._trader_payload)

    @property
    def url(self):
        return self.link

    @property
    def wiki_url(self):
        return self.wiki_link

    @property
    def updated_at(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._updated_at, "%Y-%m-%dT%H:%M:%S.%fZ")

    def _update(self, data: ItemPayload):
        self.price = data['price']
        self.base_price = data['basePrice']
        self.avg24h_price = data['avg24hPrice']
        self.avg7days_price = data['avg7daysPrice']
        self._updated_at = data['updated']
        self.diff24h = data['diff24h']
        self.diff7days = data['diff7days']

        self.icon_url = data['icon']
        self.image_url = data['imgBig']

        self._trader_payload: TraderPayload = {
            'name': data['traderName'],
            'price': data['traderPrice'],
            'currency': data['traderPriceCur']
        }

    async def update(self) -> None:
        """|coro|

        Update Item data.
        """

        http = self._http

        async with http:
            data = await http.get_item_by_uid(self.uid)

        self._update(data)


class Prefab:

    def __init__(self, prefab_type: int, payload: PrefabPayload):
        self._type: int = prefab_type
        self._update(payload)

    def _update(self, data: PrefabPayload):
        self.path = data['path']
        self.rcid = data['rcid']

    @property
    def type(self):

        types = {
            0: 'basic',
            1: 'user'
        }

        return types.get(self._type, 'Unknown Type')


class BSGItem:

    def __init__(self, payload: BSGItemPayload):
        self.raw_name: str = payload['_name']
        self.id: str = payload['_id']
        self.parent: str = payload['_parent']
        self.type: str = payload['_type']

        self.proto: str = payload.get('_proto', '')

        self._update(payload)

    def _update(self, data: BSGItemPayload) -> None:
        _props = data['_props']

        self._props = _props

        self.name = _props['Name']
        self.short_name = _props['ShortName']
        self.description = _props['Description']

        self.weight: int = _props['Weight']
        self.width: int = _props['Width']
        self.height: int = _props['Height']

        self.stack_max: int = _props['StackMaxSize']
        # self.rarity = _props['Rarity']

        self.spawn_chance: int = _props['SpawnChance']
        self.item_sound = _props['ItemSound']

        self.prefab = Prefab(0, _props['Prefab'])
        self.user_prefab = Prefab(1, _props['UsePrefab'])

        self.examine_time: int = _props['ExamineTime']

        self.loot_experience: int = _props['LootExperience']

        self.is_quest_item: bool = _props['QuestItem']

        self.fold_able: bool = _props['IsAnimated']

    @property
    def loot_exp(self) -> int:
        return self.loot_experience
