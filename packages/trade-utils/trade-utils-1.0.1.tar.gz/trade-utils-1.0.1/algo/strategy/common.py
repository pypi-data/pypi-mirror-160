import logging
from typing import Callable, Generator, NamedTuple

from algo.data.reader import PriceStream
from algo.trading import TradeResult
from algo.trading.state import CurrentState

log = logging.getLogger(__name__)
# for now money are floating... hopefully they will start soaring soon :rofl:
Money = float


class TradingResult(NamedTuple):
    profit: Money
    expenses: Money
    number_of_trades: int


BaseStrategyParams = NamedTuple


Strategy = Callable[
    [PriceStream, BaseStrategyParams, CurrentState],
    Generator[TradeResult, None, None]
]

Plan = Callable[
    [CurrentState],
    Generator[TradeResult, None, None]
]


class StrategyDescriptor(NamedTuple):
    name: str
    module: Strategy
    args: BaseStrategyParams
    description: str
