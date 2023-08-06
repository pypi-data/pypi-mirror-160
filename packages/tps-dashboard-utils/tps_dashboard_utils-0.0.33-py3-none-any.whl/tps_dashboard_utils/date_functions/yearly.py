import datetime as dt
from dateutil.relativedelta import relativedelta


def year_start(last=False):
    """
    Returns the first date of the current year by default.
    Use last=True to get the first date of the last year.
    """
    this_year = dt.date(dt.date.today().year, 1, 1)
    if last:
        return this_year + relativedelta(years=-1)
    else:
        return this_year


def year_end(last=False):
    """
    Returns the last date of the current year by default.
    Use last=True to get the last date of the previous year.
    """
    start_date = year_start(last=last)
    return start_date + relativedelta(years=1, days=-1)
