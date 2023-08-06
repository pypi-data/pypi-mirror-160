from dash import dcc
from tps_dashboard_utils.colours import categorical
import dash_bootstrap_components as dbc
import plotly.io as pio

pio.templates.default = "plotly_white"
pio.templates['plotly_white'].layout.colorway = categorical.pastel
pio.templates['plotly_white'].layout.xaxis.gridcolor = 'white'
pio.templates['plotly_white'].layout.yaxis.gridcolor = 'white'


def Dates(earliest, latest):
    date_picker = dcc.DatePickerRange(
        id='date-range',
        start_date=earliest,
        end_date=latest,
        display_format='DD-MM-YYYY',
        persistence=True,
        persisted_props=['start_date', 'end_date'],
        persistence_type='session'
    )
    return date_picker


def Navbar(service):
    navbar = dbc.NavbarSimple(
        children=[
            # dbc.NavItem(dbc.NavLink("Data refreshed: " + lastUpdate)),
            # dbc.NavItem(dbc.NavLink("Page2", href="/Page2", external_link=True)),
        ],
        brand=service,
        brand_href="/home",
        sticky="top",
        color="primary",
        dark=True,
        expand='lg',
    )
    return navbar
