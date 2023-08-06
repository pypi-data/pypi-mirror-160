from enum import Enum
from typing import NamedTuple


class OrderType(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class TradeResult(NamedTuple):
    trade_profit: float
    trade_expenses: float

    @property
    def profit(self):
        return self.trade_profit - self.trade_expenses

    def __str__(self) -> str:
        return f'<TradeResult({self.profit}):\t{self.trade_profit}\t{self.trade_expenses})>'
