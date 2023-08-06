from io import StringIO
import pandas as pd


def getData(service, csv_filename, g, dates=False, usecols=None):
    repo = g.get_repo('losthippo/tps-data')
    file = f"{service}/data/{csv_filename}"
    f = repo.get_contents(file).decoded_content
    s = str(f, 'utf-8')
    data = StringIO(s)
    return pd.read_csv(data, dayfirst=True, parse_dates=dates, usecols=usecols)