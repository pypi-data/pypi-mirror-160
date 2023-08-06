from typing import Generator, NamedTuple
import json
from datetime import datetime

from v20.pricing import ClientPrice

from algo.util import str_to_dt

JsonReadyPricePoint = tuple[str, float, float]


class PricePoint(NamedTuple):
    time: datetime
    ask: float
    bid: float

    def to_json(self) -> str:
        return json.dumps([self.time.isoformat(), self.ask, self.bid])

    def to_json_ready(self) -> JsonReadyPricePoint:
        return (self.time.isoformat(), self.ask, self.bid)

    @classmethod
    def from_json_ready(cls, data: JsonReadyPricePoint):
        return cls(*(datetime.fromisoformat(data[0]), data[1], data[2]))

    @classmethod
    def from_oanda_price(cls, data: ClientPrice):
        return PricePoint(str_to_dt(data.time), data.closeoutAsk, data.closeoutBid)


PriceStream = Generator[PricePoint, None, None]
