from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.trader import currencies, Trader as TraderPayload


class Trader:

    def __init__(self, payload: TraderPayload):
        self._update(payload)

    def _update(self, data: TraderPayload):
        name: str = data['name']

        self.name: Optional[str] = None if name == '' else name
        self.price: int = data['price']
        self.currency: currencies = data['currency']
