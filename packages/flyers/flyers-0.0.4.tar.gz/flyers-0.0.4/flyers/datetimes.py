import time
from datetime import datetime

YY_MM_DD_HH_MM_SS_FORMAT = '%Y-%m-%d %H:%M:%S'
YY_MM_DD_FORMAT = '%Y-%m-%d'
# 2021-06-20 14:00:00
STANDARD_DATETIME_FORMAT = YY_MM_DD_HH_MM_SS_FORMAT
# 2021-06-20
STANDARD_DATE_FORMAT = YY_MM_DD_FORMAT


def get_timestamp_ms():
    return int(time.time() * 1000)


def get_timestamp_ns() -> int:
    return time.time_ns()


def calc_duration(st: int) -> int:
    return get_timestamp_ms() - st


def timestamp_to_datetime_str(t, fmt=STANDARD_DATETIME_FORMAT) -> str:
    return format_datetime(datetime.fromtimestamp(t), fmt)


def timestamp_to_date_str(t, fmt=STANDARD_DATE_FORMAT):
    return format_date(datetime.fromtimestamp(t), fmt)


def parse_datetime(s: str, fmt: str = STANDARD_DATETIME_FORMAT):
    return datetime.strptime(s, fmt)


def format_datetime(d: datetime, fmt: str = STANDARD_DATETIME_FORMAT) -> str:
    return d.strftime(fmt)


def parse_date(s: str, fmt: str = STANDARD_DATE_FORMAT):
    return datetime.strptime(s, fmt)


def format_date(d: datetime, fmt: str = STANDARD_DATE_FORMAT):
    return d.strftime(fmt)


def check_datetime(s: str, fmt: str = STANDARD_DATETIME_FORMAT) -> bool:
    try:
        if not s or not isinstance(s, str) or len(s) == 0:
            return False
        parse_datetime(s, fmt)
    except ValueError:
        return False


def check_date(s: str, fmt: str = STANDARD_DATE_FORMAT) -> bool:
    return check_datetime(s, fmt)


def format_duration(st: int) -> str:
    gap = get_timestamp_ms() - st
    if gap < 1000:
        return '{}ms'.format(gap)
    elif gap < 60000:
        return '{}seconds'.format(gap / 1000)
    elif gap < 3600000:
        return '{}minutes'.format(gap / 60000)
    elif gap < 86400000:
        return '{}hours'.format(gap / 3600000)
    else:
        return '{}days'.format(gap / 86400000)
