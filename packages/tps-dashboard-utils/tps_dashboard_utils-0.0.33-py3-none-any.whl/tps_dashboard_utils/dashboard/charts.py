import plotly.graph_objects as go
import plotly.express as px

margins = go.layout.Margin(l=75, r=50, b=50, t=25)
margins_sm = go.layout.Margin(l=20, r=25, b=25, t=25)
margins_none = go.layout.Margin(l=0, r=0, b=0, t=0)


def fig_empty():
    empty = go.Figure()
    empty.update_layout(
        autosize=False,
        height=275,
        annotations=[
            dict(
                x=0.5,
                y=0.5,
                text='None in this period',
                xref='paper',
                yref='paper',
                showarrow=False,
                font={'size': 28}
            ),
        ],
        xaxis=dict(
            title="",
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            title="",
            zeroline=False,
            showticklabels=False,
        ),
    )
    return empty


def no_data_in_period_check(fig):
    if len(fig.data) > 0:
        pass
    else:
        fig = fig_empty()
    return fig


def horizontal_bars(data, x_data, y_data, label_data, height=275, category_order='total ascending', group=False, color=None, hover_data=None, hovermode=True, title=None):
    fig = px.bar(data, y=y_data, x=x_data, orientation='h', text=label_data, height=height, color=color, hover_data=hover_data, title=title)
    fig.update_xaxes(title="", showticklabels=False)
    fig.update_yaxes(title="", showticklabels=True, categoryorder=category_order)
    fig.update_layout(margin=margins)
    if group:
        fig.update_layout(barmode='group')
    if hovermode == False:
        fig.update_layout(hovermode=False)
    return no_data_in_period_check(fig)


def vertical_bars(data, x_data, y_data, label_data, height=None, color=None, category_order='trace', group=False, hover_data=None, hovermode=True, title=None):
    fig = px.bar(data, y=y_data, x=x_data, text=label_data, height=height, color=color, hover_data=hover_data, title=title)
    fig.update_xaxes(title="", showticklabels=True, categoryorder=category_order)
    fig.update_yaxes(title="", showticklabels=False)
    fig.update_layout(margin=margins)
    if group:
        fig.update_layout(barmode='group')
    if hovermode==False:
        fig.update_layout(hovermode=False)
    return no_data_in_period_check(fig)


def pie_chart(data, values, names, hole=0.5):
    fig = px.pie(data, values=values, names=names, hole=hole)
    return no_data_in_period_check(fig)
