import logging
from typing import Generator

from algo.data.reader import PriceStream
from algo.indicator import MAverage
from algo.trading.state import CurrentState
from algo.trading import OrderType, TradeResult
from algo.data.common import PricePoint
from algo.util import d
from algo.strategy.common import BaseStrategyParams


class MAStrategyParams(BaseStrategyParams):
    first_avg_length: int
    second_avg_length: int


log = logging.getLogger(__name__)


def run_trading(data_stream: PriceStream, params: MAStrategyParams, state: CurrentState) -> Generator[TradeResult, None, None]:
    (mavg1_len, mavg2_len) = params
    mavg1 = MAverage(mavg1_len)
    mavg2 = MAverage(mavg2_len)
    history_price: PricePoint
    for history_price in data_stream:
        mavg1.tick(history_price.bid)
        mavg2.tick(history_price.bid)
        log.debug('price-data', extra=d(history_price, mavg1, mavg2))
        expected_direction = None  # kind of expected price direction

        if not (mavg1.ready() and mavg2.ready()):
            # skipping before ready
            continue

        if mavg1.value > mavg2.value:
            expected_direction = OrderType.BUY
        else:
            expected_direction = OrderType.SELL

        if state.in_market and state.order_type != expected_direction:
            log.info('closing trade %s', trade)
            trade = state.close(history_price)
            yield trade

        elif not state.in_market:
            log.info('open trade %s', state)
            state.open(history_price, expected_direction)
