from typing import Optional

from algo.strategy import STRATEGIES_REGISTER, StrategyDescriptor


def get_strategy_by_name(strategy_name: str) -> Optional[StrategyDescriptor]:
    """
    TBD: move to lib
    try to conside find ... not sure wich one is more performant
    """
    for strategy in STRATEGIES_REGISTER:
        if strategy.name == strategy_name:
            return strategy
