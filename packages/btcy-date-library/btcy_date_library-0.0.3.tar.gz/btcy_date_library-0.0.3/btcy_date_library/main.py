from dateutil import tz as date_util_tz
from copy import deepcopy


def get_iso_format_time(
    datetime_naive,
    utc_str='UTC+00',
    time_str_format='%m/%d/%Y %H:%M:%S',
    offset=False,
    print_timezone=True
):
    datetime_aware = deepcopy(
        datetime_naive.replace(microsecond=0, tzinfo=date_util_tz.tzoffset(None, 0))
    )
    if not offset:
        return datetime_aware.isoformat()

    utc_int = int(utc_str.replace('UTC', ''))
    datetime_aware_tz_offset = datetime_aware.astimezone(tz=date_util_tz.tzoffset(None, utc_int * 3600))
    if time_str_format:
        if print_timezone:
            return datetime_aware_tz_offset.strftime(time_str_format) + ' ({:+03d}:00)'.format(utc_int)
        else:
            return datetime_aware_tz_offset.strftime(time_str_format)
    else:
        return datetime_aware_tz_offset.isoformat()