import datetime as dt
from dateutil.relativedelta import relativedelta


def start(last=False):
    """
    Returns the first date of the current month by default.
    Use last=True to get the first date of last month.
    """
    today = dt.date.today()
    start_date = dt.date(today.year, today.month, 1)
    if last:
        return start_date + relativedelta(months=-1)
    return start_date


def end(last=False):
    """
        Returns the last date of the current month by default.
        Use last=True to get the last date of the previous month.
        """
    return start(last=last) + relativedelta(months=1, days=-1)
