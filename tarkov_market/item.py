from __future__ import annotations
from typing import List, TYPE_CHECKING

import datetime

from .traders import Trader

if TYPE_CHECKING:
    from .types.item import (
        Item as ItemPayload,
        BSGItem as BSGItemPayload,
        BSGPrefab as PrefabPayload,
        BSGProps
    )

__all__ = (
    'Item',
    'BSGItem'
)


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
        'is_functional',
        'tags',
        'trader',
        '_http',
        'banned_on_flea',
        'have_market_data',
    )

    def __init__(self, payload: ItemPayload):
        self.uid: str = payload['uid']
        self.bsg_id: str = payload['bsgId']
        self.name: str = payload['name']
        self.short_name: str = payload['shortName']
        self.slots: int = payload['slots']
        self.link: str = payload['link']
        self.wiki_link: str = payload['wikiLink']

        self._update(payload)

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.price

    def __eq__(self, other) -> bool:
        return isinstance(other, Item) and self.uid == other.uid

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        attrs = (
            ('uid', self.uid),
            ('name', self.name),
            ('price', self.price),
            ('short_name', self.short_name),
            ('banned_on_flea', self.banned_on_flea),
        )

        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'

    def __hash__(self) -> int:
        return hash(self.uid)

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

        self.is_functional: bool = data['isFunctional']
        self.tags: List[str] = data['tags']

        self.trader: Trader = Trader(data)

        self.banned_on_flea: bool = data['bannedOnFlea']
        self.have_market_data: bool = data.get('haveMarketData', False)


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

        self._update(payload['_props'])

    def _update(self, data: BSGProps) -> None:
        self.name = data.get('Name')
        self.short_name = data.get('ShortName')
        self.description = data.get('Description')

        self.weight: int = data.get('Weight')
        self.width: int = data.get('Width')
        self.height: int = data.get('Height')

        self.stack_max: int = data.get('StackMaxSize')
        self.rarity = data.get('spawnRarity')

        self.item_sound = data.get('ItemSound')

        prefab = data.get('Prefab')
        use_prefab = data.get('UsePrefab')

        self.prefab = Prefab(0, prefab) if prefab else None
        self.use_prefab = Prefab(1, use_prefab) if use_prefab else None

        self.examine_time: int = data.get('ExamineTime')

        self.loot_experience: int = data.get('LootExperience')

        self.is_quest_item: bool = data.get('QuestItem')

        self.fold_able: bool = data.get('IsAnimated', False)

        self.repair_cost: int = data.get('RepairCost', 0)
        self.repair_speed: int = data.get('RepairSpeed', 0)

        self.credits_price: int = data.get('CreditsPrice', 0)

    @property
    def loot_exp(self) -> int:
        return self.loot_experience
