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
from django.db.models import Q


RATES = range(1, 6)
styles = {
    'app':{
        'height': '100%',
        'width': '100%',
        'overflowX': 'show',
        'overflowY': 'show'
        }
    }
app = DjangoDash('defplot', add_bootstrap_links=True)
app.layout = html.Div([
    dcc.Input(id='df_inp', type="hidden", style={"display": "hidden"}),
    dcc.Store(id="cache", data=[]),
    html.H1("Shiftplan Preview", style={"text-align": "center"}),
    html.Div([
            html.Pre(id='click-data', children=[]),
    ], className='three columns'),
    html.Br(),
    dcc.Graph(id="chart_plot")
], style=styles['app'])


@app.callback(
    Output('chart_plot', 'figure'),
    [Input('df_inp', 'value')])
def generate_graph(df_inp, session_state=None, *args, **kwargs):
    if df_inp is None:
        django_dash = kwargs["request"].session.get("django_dash")
        df = pd.read_json(django_dash.get('df'))
        df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
        df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    else:
        df = pd.read_json(df_inp)
        df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
        df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    # print("generae_graph", df)
    dff = df.copy()
    fig = chart_plot(dff)
    fig.update_layout(clickmode='event+select')
    return fig

@app.callback(
    Output('click-data', 'children'),
    Input('chart_plot', 'clickData'),
    State('df_inp', 'value'))
def display_click_data(clickData, df_inp):
    if clickData:
        clicked_point = clickData["points"][0]
        # print("clickData: ", clickData)
        jt_name = clicked_point["label"]
        begin_dt = datetime.fromisoformat(clicked_point["base"])
        end_dt = datetime.fromisoformat(clicked_point["value"])
        # during = end_dt - begin_dt
        # print(begin_dt.date(), end_dt.date())
        if begin_dt.date() == end_dt.date():
            body_text = html.Div([
                html.B('{date}'.format(date=begin_dt.date())),
                html.P('{begin} - {end}'.format(begin=begin_dt.time().strftime("%H:%M"), end=end_dt.time().strftime("%H:%M"))),
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
                    '{time}'.format(time=end_dt.time().strftime("%H:%M"))
                    ]),
            ]
            )
        modal = html.Div(
            [
                # dbc.Button("Open modal", id="open", n_clicks=0), 
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            dbc.ModalTitle("{name}".format(name=jt_name)),
                            close_button=False),
                        dbc.ModalBody(body_text),
                        dbc.ModalFooter(
                            dbc.Button("Close",
                                id={
                                    'type': 'close_modal',
                                    'index': clicked_point["pointIndex"]
                                }
                            )#,
                            # dbc.Button("Update Job",
                            #     id={
                            #         'type': 'update_job',
                            #         'index': clicked_point["pointIndex"]
                            #     }
                            # )
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
    Output("modal", "is_open"),
    Input({'type': 'close_modal', 'index': ALL}, 'n_clicks'),
    # Input({'type': 'update_job', 'index': ALL}, 'n_clicks'),
    State('df_inp', 'value'))
def close_modal(close_modal, df_inp, *args, **kwargs):
    if close_modal != [None] and kwargs['callback_context'].triggered != []:
        return False
    return True
    

def chart_plot(df):
    """
    Returns timeline plot.
    @param df: input df
    TODO: discrete color map and legend.
    """
    rating_color_map = {
        1: "green",
        2: "yellow",
        3: "orange",
        4: "goldenrod",
        5: "red"
        }
    # rating_color_map = {str(i): rating_color_map[i] for i in rating_color_map}
    tl = px.timeline(
        df, x_start="begin", x_end="end", y="name", color="default_rating", opacity=0.5, labels={})
    tl.update_traces(marker_line_color='rgb(0,0,0)', marker_line_width=3, opacity=1)
    tl.update_yaxes(autorange="reversed")
    return tl
