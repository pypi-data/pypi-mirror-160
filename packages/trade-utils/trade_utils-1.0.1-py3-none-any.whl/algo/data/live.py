import logging

import v20
from v20.pricing import ClientPrice, PricingHeartbeat

from algo.config import config
from algo.data.reader import PricePoint
from algo.constant import Symbol
from algo.util import d


log = logging.getLogger(__name__)


def price_to_dict(price: ClientPrice):
    return {
        'type': type(price).__name__,
        'instrument': price.instrument,
        'time': price.time,
        # see main.py for traceback related to this line
        'bid': price.bids[0].price,
        'ask': price.asks[0].price,
        'all-bids': price.bids,
        'all-asks': price.asks,
        'closeoutAsk': price.closeoutAsk,
        'closeoutBid': price.closeoutBid,
        'dict': price.dict()
    }


def heartbeat_to_dict(heartbeat: PricingHeartbeat):
    return {
        'type': heartbeat.type,
        'time': heartbeat.time,
        'dict': heartbeat.dict()
    }


def get_prices_generator(stream):
    for msg_type, msg in stream.parts():
        log.debug(
            'got message', extra={
                'message_type': msg_type,
                'dict': msg.dict()
            }
        )

        if msg_type == 'pricing.PricingHeartbeat':
            log.debug('pricing.PricingHeartbeat', extra=heartbeat_to_dict(msg))
        elif msg_type == 'pricing.ClientPrice':
            log.debug('pricing.ClientPrice', extra=price_to_dict(msg))
            yield PricePoint.from_oanda_price(msg)
        else:
            log.info('unexpected-stream-message', extra=d(msg))


def get_live_price_stream(symbol: Symbol):
    api = v20.Context(
        hostname=config.oanda_stream_host_name,
        token=config.oanda_token,
    )

    stream = api.pricing.stream(
        accountID=config.oanda_account_id,
        instruments=symbol.value,
        snapshot=True
    )

    yield from get_prices_generator(stream)
