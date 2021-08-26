from __future__ import annotations
from typing import TYPE_CHECKING

import datetime

from .traders import Trader

if TYPE_CHECKING:
    from .types.item import Item as ItemPayload
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
        '_trader_payload'
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
