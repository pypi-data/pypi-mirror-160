import logging
from typing import List

from v20 import Context
from v20.order import MarketOrder
from v20.response import Response
from v20.trade import Trade

# should be from algo.config, but autofromatter keeps me in a hostage
from algo.config import config
from algo.trading import OrderType
from algo.constant import Symbol  # issues with
from algo.util import d
# from http import HttpStatus

log = logging.getLogger(__name__)


class RestApi:
    @staticmethod
    def get_rest_api():
        return Context(
            hostname=config.oanda_rest_host_name,
            token=config.oanda_token,
        )

    def __init__(self, default_instrument: Symbol) -> None:
        self._api = self.get_rest_api()
        # keep as a copy to shorten all API call
        self._account_id = config.oanda_account_id
        self._default_instrument = default_instrument

    def open(self, direction: OrderType):
        order_spec: MarketOrder = MarketOrder(
            type='MARKET',  # MARKET is a default value
            instrument=self._default_instrument.value,
            # positive buy, negative - sell
            units=1 if direction == OrderType.BUY else -1
        )

        response: Response = self._api.order.create(
            accountID=self._account_id,
            order=order_spec
        )
        log.info('open-order-response', extra=d(response))

    def close_all_trades(self):
        for trade in self.get_open_trades():
            log.info('closing trade', extra=d(trade))
            self.close_trade(trade.id)

    def close_trade(self, trade_id):
        response = self._api.trade.close(
            accountID=self._account_id,
            tradeSpecifier=trade_id
        )
        log.info('close-trade-response', extra=d(response))

    def get_open_trades(self) -> List[Trade]:
        response: Response = self._api.trade.list_open(
            accountID=self._account_id
        )
        log.info('get-open-trades-response', extra=d(response))
        return response.body['trades']
