
from datetime import datetime

import rfc3339
import iso8601


def format_vars(*args, **kwargs):
    """
    method to shorten dubug ie
    log.info('message', extra=d(1))
    instead of
    log.info('message', extra={'v': 1})
    """
    return {'a': args, 'kwa': kwargs}


d = format_vars


def is_dt_naive(dt_value: datetime) -> bool:
    """ checks that datetime doesn't have tz information """
    return dt_value.tzinfo is None or dt_value.tzinfo.utcoffset(d) is None


def dt_to_rfc3339(dt_value: datetime) -> str:
    """
    reverse: iso8601.parse_date(date_string)
    """
    return rfc3339.rfc3339(dt_value)


def str_to_dt(dt_str: str) -> datetime:
    return iso8601.parse_date(dt_str)


def now():
    """ used mostly in tests, so timezone must be but it doesn't really matter """
    return datetime.utcnow()
