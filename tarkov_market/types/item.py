from typing import Literal
from .trader import _RawTrader

LangType = Literal['en', 'ru', 'de', 'fr', 'es', 'cn']


class Item(_RawTrader):
    uid: str
    bsgId: str
    name: str
    shortName: str
    price: int
    basePrice: int
    avg24hPrice: int
    avg7daysPrice: int
    updated: str
    slots: int
    diff24h: int
    diff7days: int
    icon: str
    link: str
    wikiLink: str
    img: str
    imgBig: str
    reference: str
