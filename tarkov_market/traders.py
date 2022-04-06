from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.trader import currencies, Trader as TraderPayload


class Trader:

    def __init__(self, payload: TraderPayload):
        self._update(payload)

    def __str__(self) -> str:
        return self.name

    def _update(self, data: TraderPayload):
        name: str = data['traderName']

        self.name: Optional[str] = None if name == '' else name
        self.price: int = data['traderPrice']
        self.currency: currencies = data['traderPriceCur']
        self.ruble_price: int = data['traderPriceRub']
