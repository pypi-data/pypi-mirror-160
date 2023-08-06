import datetime as dt
from dateutil.relativedelta import relativedelta


def start(last=False):
    """
    Returns the date of the first day of the week.
    Will use the current week by default. Use last=True to get the first
    date of last week.
    """
    today = dt.date.today()
    day_of_week = today.weekday()  # gets the number of the current day
    start_date = today - relativedelta(days=day_of_week)
    if last:
        return start_date - relativedelta(days=7)
    else:
        return start_date


def end(last=False):
    """
    Returns the date of the last day of the week.
    Uses the current week by default. Use last=True to get the last
    date of the previous week.
    """
    first_day = start(last=last)
    return first_day + relativedelta(days=6)


def days_MS():
    return ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']