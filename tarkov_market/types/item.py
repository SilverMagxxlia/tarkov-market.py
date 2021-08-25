from typing import Literal, TypedDict

LangType = Literal['en', 'ru', 'de', 'fr', 'es', 'cn']


class Trader(TypedDict, total=False):
    traderName: str
    traderPrice: int
    traderPriceCur: str


class Item(Trader):
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
