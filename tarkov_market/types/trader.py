from typing import TypedDict, Literal

currencies = Literal['₽', '$', '€']


class Trader(TypedDict, total=False):
    traderName: str
    traderPrice: int
    traderPriceCur: currencies
    traderPriceRub: int
