import datetime as dt
from dateutil.relativedelta import relativedelta


def current_quarter():
    """
    Returns the number of the current quarter
    """
    return (dt.date.today().month - 1) // 3 + 1


def start(last=False):
    """
    Returns the first date of the current quarter by default.
    Use last=True to get the first date of the last quarter.
    """
    quarter = current_quarter()
    if last:
        quarter -= 1
    return dt.date(dt.date.today().year, 3 * quarter - 2, 1)


def end(last=False):
    """
    Returns the last date of the current quarter by default.
    Use last=True to get the last date of the previous quarter.
    """
    start_date = start(last=last)
    return start_date + relativedelta(months=3, days=-1)

