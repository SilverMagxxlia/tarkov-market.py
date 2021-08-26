from typing import TypedDict, Literal

currencies = Literal['₽', '$', '€']


class _RawTrader(TypedDict, total=False):
    traderName: str
    traderPrice: int
    traderPriceCur: currencies


class Trader(TypedDict, total=False):
    name: str
    price: int
    currency: currencies
