from textwrap import fill
from dash import html
from io import StringIO
import pandas as pd
import numpy as np
import json


def strip_whitespace(df):
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    return df


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


def age_bins(df, col):
    bins = pd.cut(df[col], [0, 24, 34, 44, 54, 64, np.inf], labels=['16-24', '25-34', '35-44', '45-54', '55-64', '65+'])
    return bins


def label(df, numerator, denominator=False):
    """ Function that takes a dataframe and a column of values and \
    generates a percentage that each value represents. \
    It also then combines these into a label that can be used for charting.

    Denominator can be specified if the calculation should be as a percentage
    of a particular variable, e.g. number of clients that were worked with in a period
    instead of the total in the dataframe
    """
    if denominator:
        df['P'] = round(df[numerator] * 100 / denominator, 2)
    else:
        df['P'] = round(df[numerator] * 100 / df[numerator].sum(), 2)
    df['Label'] = df[numerator].map(str) + " (" + df['P'].map(str) + "%)"
    return df


def business_minutes(start, end, biz_hours=pd.offsets.BusinessHour()):
    times_array = pd.date_range(start, end, freq='min')
    times = pd.DataFrame(times_array, columns=['timestamp'])
    times['IsBizMin'] = times['timestamp'].apply(pd.Timestamp).apply(biz_hours.is_on_offset)
    
    biz_min = times.IsBizMin.sum() 
    
    if biz_min != 0:
        return biz_min -1
    
    else:
        return biz_min


def non_business_minutes(start, end, biz_hours=pd.offsets.BusinessHour()):
    times_array = pd.date_range(start, end, freq='min')
    times = pd.DataFrame(times_array, columns=['timestamp'])
    times['IsBizMin'] = times['timestamp'].apply(pd.Timestamp).apply(biz_hours.is_on_offset)
    
    non_biz_min = len(times) - times.IsBizMin.sum() 
    
    if non_biz_min != 0:
        return non_biz_min -1
    
    else:
        return non_biz_min


def calculate_outside_hours(df, start, end):
    biz_hours = pd.offsets.BusinessHour()
    in_hours = []
    outside_hours = []

    for index, row in df.iterrows():
        # Create an array of minutes that the start and end time covers
        times_array = pd.date_range(start=row[start],
                                    end=row[end],
                                    freq='min')
        # Create a df from the array
        times = pd.DataFrame(times_array, columns=['timestamp'])

        # Check whether each minute is in business time or not
        times['IsBizHour'] = times['timestamp'].apply(pd.Timestamp).apply(biz_hours.is_on_offset)

        # Create an array of the number of hours outside business hours
        outside_hours.append((len(times) - times.IsBizHour.sum()) / 60)

    # Sum the hours outside and return the number
    return sum(outside_hours)


def load_callback_data(datasets, data):
    my_data = json.loads(datasets)
    return pd.read_json(my_data[data], orient="split", convert_dates=True)


def create_csv(name_string, datasets, data, start_date, end_date, columns_to_include=False, columns_to_ignore=False):
    filename = f"{name_string} - {str(start_date)} to {str(end_date)}.csv"
    s = StringIO()

    df = load_callback_data(datasets, data)
    if columns_to_include:
        df = df[columns_to_include].reset_index(drop=True)
    if columns_to_ignore:
        df = df.loc[:, ~df.columns.isin(columns_to_ignore)].reset_index(drop=True)

    df.to_csv(s, index=False)
    content = s.getvalue()
    return dict(filename=filename, content=content, type="text/csv")


def group_count_and_label(data, group_by, aggregation={'POEID':'count'}, index='POEID', apply_label=True, simple=False, n=5, denominator=False, dropna=True, reindex=False):
    df = data.groupby(group_by, dropna=dropna).agg(aggregation).reset_index()
    
    if reindex:
        df = data.groupby(group_by, dropna=dropna).agg(aggregation).reindex(reindex, fill_value=0).reset_index()
    else:
        pass
    
    if simple:
        df = df.replace(df.groupby(group_by, dropna=dropna).sum().sort_values(index, ascending=False).index[n:], 'Other') \
            .groupby(group_by).sum().reset_index()
    else:
        pass

    if apply_label:
        df = label(df=df, numerator=index, denominator=denominator)
    else:
        pass

    return df


def get_engagement_types(df, column, startswith):
    dff = df[df[column].str.startswith(startswith)]
    dff[column] = dff[column].str.replace(startswith, '')
    return dff.reset_index(drop=True)


def group_by_week(df, date_column, count_column='POEID'):
    return df.groupby(pd.Grouper(key=date_column, freq='W-MON'))[[count_column]].count().reset_index()
