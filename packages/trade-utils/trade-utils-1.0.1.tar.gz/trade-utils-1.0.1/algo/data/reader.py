import logging
from datetime import datetime, timedelta

from influxdb.resultset import ResultSet

from algo.config import config
from algo.constant import Symbol
from algo.util import d, dt_to_rfc3339
from algo.data.cache import cached
from algo.data.common import PricePoint, PriceStream
from algo.data.connection import DataConnection

log = logging.getLogger(__name__)


class DataReader(DataConnection):
    def __init__(self, url, token, org):
        super().__init__(url, token, org)
        self._query_api = self._client.query_api()

    def hour_data(self, date_str: str, symbol: Symbol) -> PriceStream:
        start = datetime.fromisoformat(date_str)
        end = start + timedelta(hours=1)
        yield from cached(
            f'hour-data-{symbol.value}-{start.isoformat()}',
            self.get_data_stream(start, end, symbol)
        )

    def day_data(self, date_str: str, symbol: Symbol) -> PriceStream:
        start = datetime.fromisoformat(date_str)
        end = start + timedelta(days=1)
        yield from cached(
            f'day-data-{symbol.value}-{start.isoformat()}',
            self.get_data_stream(start, end, symbol)
        )

    def week_data_direct(self, date_str: str, symbol: Symbol) -> PriceStream:
        week_dt = datetime.fromisoformat(date_str)
        start = week_dt - timedelta(days=week_dt.weekday())
        end = start + timedelta(days=6)
        yield from cached(
            f'week-data-{symbol.value}-{start.isoformat()}',
            self.get_data_stream(start, end, symbol)
        )

    def week_data(self, date_str: str, symbol: Symbol) -> PriceStream:
        week_dt = datetime.fromisoformat(date_str)
        start = week_dt - timedelta(days=week_dt.weekday())
        end = start + timedelta(days=6)
        # 1 weeek data set is too big to cache at this point so doing it iteratively
        current_day = start
        while current_day <= end:
            log.info('getting data for the day', extra=d(current_day))
            yield from self.day_data(current_day.isoformat(), symbol)
            current_day += timedelta(days=1)

    def get_result_set(self, symbol: Symbol, start: datetime, end: datetime) -> ResultSet:
        query_str = f"""
            from(bucket: "tsdata")
              |> range(start: {dt_to_rfc3339(start)}, stop: {dt_to_rfc3339(end)})
              |> filter(fn: (r) => r["instrument"] == "{symbol.value}")
              |> filter(fn: (r) => r["_measurement"] == "price")
              |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
        """
        return self._query_api.query(query_str)

    def get_data_stream(
            self, start: datetime, end: datetime, symbol: Symbol
    ) -> PriceStream:
        log.debug('getting chunk starting', extra=d(start))
        results = self.get_result_set(symbol, start, end)
        log.info('query-result', extra={'r': results})
        for flux_table in results:
            for record in flux_table:
                yield PricePoint(record['_time'], record['ask'], record['bid'])

    def get_data_stream_iterative_ready(
            self, start: datetime, end: datetime, symbol: Symbol
    ) -> PriceStream:
        """
        not in use consider removal
        """
        current_start = start
        keep_loading = True
        while keep_loading and current_start < end:
            log.debug('getting next chunk %s', current_start)
            results = self.get_result_set(symbol, current_start, end)
            log.info('query-result', extra={'r': results})
            for flux_table in results:
                for record in flux_table:
                    # following extra condition is present due to milliseconds round up of the influx
                    keep_loading = current_start <= record['_time']
                    if keep_loading:
                        current_start = record['_time']
                        log.info('current_start', extra=d(start=current_start))
                        yield PricePoint(record['_time'], record['ask'], record['bid'])


def get_data_reader() -> DataReader:
    return DataReader(
        config.influx_url,
        config.influx_token,
        config.influx_org
    )
