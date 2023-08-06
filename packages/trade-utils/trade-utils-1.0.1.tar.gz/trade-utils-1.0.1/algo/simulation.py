import logging
from functools import partial

from algo.constant import Symbol
from algo.data.common import PriceStream
from algo.data.reader import get_data_reader
from algo.strategy.common import (BaseStrategyParams, Plan, Strategy,
                                  TradingResult)
from algo.trading.state import CurrentState

log = logging.getLogger(__name__)


def plan_strategy(strategy: Strategy, price_stream: PriceStream, params: BaseStrategyParams) -> Plan:
    return partial(strategy, price_stream, params)


def run_simulation(plan: Plan) -> TradingResult:
    trades = []
    state = CurrentState()
    for trade in plan(state):
        trades.append(trade)

    total_profit = sum(tr.profit for tr in trades)
    total_expenses = sum(tr.trade_expenses for tr in trades)
    num_of_trades = len(trades)
    log.info('simulation total',
             extra={
                 'trades_len': num_of_trades,
                 'total_profit': total_profit,
                 'sum_of_expenses': total_expenses
             })
    return TradingResult(total_profit, total_expenses, num_of_trades)


def simulate_trading(simulation_date: str, symbol: Symbol, strategy: Strategy, params: BaseStrategyParams):
    """ This method is used by trainer"""
    log.info('start simulation')
    data_reader = get_data_reader()
    data_iterator = data_reader.week_data(simulation_date, symbol)
    planned_strategy = plan_strategy(strategy, data_iterator, params)

    result = run_simulation(planned_strategy)

    log.info('simulation result', extra={'simulation-result': result})
    return result
