import re
import datetime


def check_datetime_format(time: str):
    return datetime.datetime.strptime(time[:-1], '%Y-%m-%dT%H:%M:%S.%f')


def check_time_format(hours: str):
    pattern = r'^(\d|[01]\d|2[0-3]):([0-5]\d)-(\d|[01]\d|2[0-3]):([0-5]\d)$'
    if re.match(pattern, hours):
        return hours
    else:
        raise ValueError(f'{hours} - wrong time format')
