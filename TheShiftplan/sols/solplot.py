import json
import pandas as pd
from datetime import datetime

from dash import dcc, html, ctx, MATCH, ALL
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.offline import plot
import chart_studio.plotly as py
import chart_studio
chart_studio.tools.set_config_file(world_readable=False, sharing='private')
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash

from django.contrib.auth.models import User
from defs.models import Jobtype, Job
from prefs.models import UserJobRating
from django.db.models import Q

from utils import config 


PLOT_MODE_OPTIONS = [
    {'label': "Show only my assigned jobs.", 'value': "user_assigned"},
    # {'label': "Show my assigned jobs", 'value': "assigned_rating"},
    {'label': "Show all assigned jobs.", 'value': "all_assigned"}
]
COLOR_MODE_OPTIONS = [
    {'label': "Own rating", 'value': "user_rating"},
    {'label': "Assigned Rating", 'value': "assigned_rating"},
    {'label': "Popularity", 'value': "popularity"}
]
RATES = range(1, 6)
styles = {
    'app':{
        'height': '100%',
        'width': '100%',
        'overflowX': 'show',
        'overflowY': 'show'
        }
    }
app = DjangoDash('solplot', add_bootstrap_links=True)
app.layout = html.Div([
    dcc.Input(id='df_inp', type="hidden", style={"display": "hidden"}),
    dcc.Input(id='is_admin', type="hidden", style={"display": "hidden"}),
    dcc.Store(id="cache", data=[]),
    html.Div([
        html.Label(
            children="Select Plot Mode.",
            htmlFor="plot_mode"
        ),
        dcc.Dropdown(
            id="plot_mode",
            options=PLOT_MODE_OPTIONS,
            value="user_assigned",
            multi=False,
            clearable=False,
            style={'width': '49%', "position": "relative"},
            maxHeight=500,
            className="mode dropdown"
        ),
        html.Label(
            children="Select Color Mode.",
            htmlFor="color_mode"
        ),
        dcc.Dropdown(
            id="color_mode",
            options=COLOR_MODE_OPTIONS,
            value="assigned_rating",
            multi=False,
            clearable=False,
            style={'width': '49%', "position": "relative"},
            maxHeight=500,
            className="mode dropdown"
        )
    ]),
    html.Div([
            dcc.Markdown("""
                **Click Data**
                Click on points in the graph.
            """),
            html.Pre(id='click-data', children=[]),
    ], className='three columns'),
    html.Br(),
    dcc.Graph(id="chart_plot")
], style=styles['app'])


# @app.callback(
#     Output('is_admin', 'value'),
#     Output('plot_mode', 'value'),
#     Output('color_mode', 'value'),
#     State('is_admin', 'value')
#     )
# def set_is_admin(is_admin, *args, **kwargs):
#     django_dash = kwargs["request"].session.get("django_dash")
#     session_is_admin = django_dash.get("is_admin")
#     if session_is_admin:
#         plot_mode = "all_assigned"
#     else:
#         plot_mode = "user_assigned"
#     color_mode = "assigned_rating"
#     return session_is_admin, plot_mode, color_mode


@app.callback(
    Output('chart_plot', 'figure'),
    [Input('df_inp', 'value'),
    Input('color_mode', 'value'),
    Input('plot_mode', 'value')
    ])
def generate_graph(df_inp, color_mode, plot_mode, session_state=None, *args, **kwargs):
    django_dash = kwargs["request"].session.get("django_dash")
    current_username = django_dash.get('username')
    if df_inp is None:
        df = pd.read_json(django_dash.get('df'))
        df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
        df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    else:
        df = pd.read_json(df_inp)
        df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
        df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    # print("generae_graph", df)
    if plot_mode == "user_assigned":
        # print(df.loc[df["assigned_username"] == current_username])
        df = df.loc[df["assigned_username"] == current_username]
    dff = df.copy()
    fig = chart_plot(dff, color_mode)
    fig.update_layout(clickmode='event+select')
    return fig


@app.callback(
    Output('click-data', 'children'),
    Input('chart_plot', 'clickData'),
    State('df_inp', 'value'),
    State('color_mode', 'value'),
    State('is_admin', 'value')
    )
def display_click_data(clickData, df_inp, color_mode, is_admin):
    if clickData:
        clicked_point = clickData["points"][0]
        # print("clickData: ", clickData)
        # print(clicked_point)
        jt_name = clicked_point["label"]
        begin_dt = datetime.fromisoformat(clicked_point["base"])
        end_dt = datetime.fromisoformat(clicked_point["value"])
        during = end_dt - begin_dt
        
        assigned_user = clicked_point["text"]
        rating = clicked_point["customdata"][1]
        if color_mode == "popularity":
            visible_rating = f"- Popularity: {rating}"
        elif color_mode == "assigned_rating":
            visible_rating = f"rated with a: {rating}"
        elif color_mode == "user_rating":
            visible_rating = f"- my rating: {rating}"
        # print(begin_dt.date(), end_dt.date())
        if begin_dt.date() == end_dt.date():
            body_text = html.Div([
                html.B('{date}'.format(date=begin_dt.date())),
                html.P('{begin} - {end} ({during})'.format(begin=begin_dt.time().strftime("%H:%M"), end=end_dt.time().strftime("%H:%M"), during=during)),
            ]
            )
        else:
            body_text = html.Div([
                html.P([
                    html.B('{date} '.format(date=begin_dt.date())),
                    '{time}'.format(time=begin_dt.time().strftime("%H:%M"))
                    ]),
                html.P([
                    html.B('{date} '.format(date=end_dt.date())),
                    '{time} ({during})'.format(time=end_dt.time().strftime("%H:%M"), during=during)
                    ]),
            ])
        modal = html.Div(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            dbc.ModalTitle(f"{assigned_user} {visible_rating}")
                        ),
                        dbc.ModalBody(body_text),
                        dbc.ModalFooter(
                            dbc.Button("Close",
                                id={
                                    'type': 'close_modal',
                                    'index': clicked_point["customdata"][0]
                                }
                            )
                        ),
                    ],
                    id="modal",
                    is_open=True,
                    keyboard=False,
                    backdrop="static",
                ),
            ]
        )
        return modal


@app.callback(
    Output('df_inp', 'value'),
    Output("modal", "is_open"),
    Input({'type': 'close_modal', 'index': ALL}, 'n_clicks'),
    State('df_inp', 'value'))
def close_modal(close_modal, df_inp, *args, **kwargs):
    # print("close_modal, submit_form")
    # print(close_modal, submit_form)
    django_dash = kwargs["request"].session.get("django_dash")
    df_json = django_dash.get("df")
    # print(df_json)
    if close_modal != [None] and kwargs['callback_context'].triggered != []:
        return df_inp, False
    print("noch nicht")
    return df_inp, True


def chart_plot(df, color_mode):
    """
    Returns timeline plot.
    @param df: input df, color_mode
    TODO: discrete color map and legend.
    """
    df["assigned_rating"] = df["assigned_rating"].astype(str)
    df["user_rating"] = df["user_rating"].astype(str)
    rating_color_map = {
        0: "grey",
        1: "green",
        2: "yellow",
        3: "orange",
        4: "goldenrod",
        5: "red"
        }
    rating_color_map = {str(i): rating_color_map[i] for i in rating_color_map}
    sorted_jobtype_names = list(df["name"])
    sorted_jobtype_names.sort()
    if color_mode == "popularity":
        tl = px.timeline(
            df,
            x_start="begin",
            x_end="end",
            y="name",
            color="popularity",
            opacity=0.5,
            labels={},
            text="assigned_username",
            category_orders={
                "name": sorted_jobtype_names
            },
            custom_data=["job", "popularity"]
        )
    elif color_mode == "assigned_rating":
        tl = px.timeline(
            df,
            x_start="begin",
            x_end="end",
            y="name",
            color="assigned_rating",
            opacity=0.5,
            labels={},
            text="assigned_username",
            color_discrete_map=rating_color_map,
            category_orders={
                "assigned_rating": rating_color_map.keys(),
                "name": sorted_jobtype_names
            },
            custom_data=["job", "assigned_rating"]
        )
    elif color_mode == "user_rating":
        tl = px.timeline(
            df,
            x_start="begin",
            x_end="end",
            y="name",
            color="user_rating",
            opacity=0.5,
            labels={},
            text="assigned_username",
            color_discrete_map=rating_color_map,
            category_orders={
                "user_rating": rating_color_map.keys(),
                "name": sorted_jobtype_names
            },
            custom_data=["job", "user_rating"]
        )
    tl.update_traces(marker_line_color='rgb(0,0,0)', marker_line_width=3, opacity=1)    
    return tl