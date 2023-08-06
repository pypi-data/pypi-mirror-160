#!/usr/bin/python3

# import json
import logging.config

# from algo.config import config
from algo.constant import Symbol
# from algo.data.reader import PriceStream, get_data_reader
from algo.simulation import simulate_trading
# from algo.strategy.moving_averages import MAStrategyParams, run_simulation
# from algo.trading import PricePoint
# from algo.util import d, now
from algo.strategy import moving_average_sample

logging.config.fileConfig(
    './logging.conf',
    # TBD: figure out why lack of the following line disables logging inside module
    disable_existing_loggers=False
)

log = logging.getLogger(__name__)


# def serialize_data_record(data_record):
#     """
#     input is a FluxRecord
#     """
#     return data_record['result']['_measurement']


# def read_all(data: PriceStream):
#     data_points_counter = 0
#     total_length = 0  # in chars
#     total_ask = 0.0
#     total_bid = 0.0
#     for data_point in data:
#         # log.info('data-point', extra=d(data_point))
#         # log.info('data-point', extra=d(data_point[0].isoformat()))
#         total_ask += data_point[1]
#         total_bid += data_point[2]

#         data_serialized = data_point.to_json()
#         total_length += len(data_serialized)
#         data_points_counter += 1
#     return data_points_counter, total_length, total_ask, total_bid


if __name__ == '__main__':
    log.info('playground home will be here')
    # price_generator = (
    #     PricePoint(now(), 1, 2),
    #     PricePoint(now(), 2, 3),
    #     PricePoint(now(), 3, 4),
    #     PricePoint(now(), 5, 6),
    # )
    # run_simulation(price_generator, MAStrategyParams(1, 2))
    # data_reader = get_data_reader()

    # data_iterator = data_reader.day_data(
    #     '2022-06-20 00:00:00+00:00', Symbol.JPY)
    # log.info('start-reading')
    # data_stat = read_all(data_iterator)
    # log.info('data-stat', extra=d(data_stat))
    # log.info('first-read-complete')
    # data_iterator = data_reader.day_data(
    #     '2022-06-20 00:00:00+00:00', Symbol.JPY)
    # log.info('start-second-reading')
    # data_stat = read_all(data_iterator)
    # log.info('data-stat', extra=d(data_stat))
    # log.info('second-read-complete')

    strategy = moving_average_sample
    result = simulate_trading(
        '2022-06-20',
        Symbol.JPY,
        strategy.module,
        strategy.args(2, 3)
    )
    log.info('simulation-complete', extra={'result': result})
