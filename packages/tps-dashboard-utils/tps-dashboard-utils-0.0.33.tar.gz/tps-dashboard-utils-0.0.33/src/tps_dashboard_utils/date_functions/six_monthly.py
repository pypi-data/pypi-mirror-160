from dateutil.relativedelta import relativedelta
from tps_dashboard_utils.date_functions import monthly


def start(last=False):
    """
    Used to get 6 whole months of data. Uses the current month-6 by default
    but will use the last month - 6 if last=True
    """
    start_date = monthly.start(last=last)
    return start_date + relativedelta(months=-6)


def six_month_end(last=False):
    """
    Used to get 6 whole months of data. Uses the current month-6 by default
    but will use the last month - 6 if last=True
    """
    start_date = start(last=last)
    return start_date + relativedelta(months=6, days=-1)
