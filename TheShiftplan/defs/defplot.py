import json
import pandas as pd
from datetime import datetime, date
from collections import OrderedDict

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

import logging

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


def create_form_modal_body(clicked_point):
    # print(clicked_point)
    jt_name = clicked_point["label"]
    begin_dt = datetime.fromisoformat(clicked_point["base"])
    end_dt = datetime.fromisoformat(clicked_point["value"])
    body_text = html.Div([
        html.Label(
            children = "Start: ",
            className = "modal_input_label"

        ),
        dcc.DatePickerSingle(
            id={
                'type': 'begin_date',
                'index': clicked_point["customdata"][0]
            },
            min_date_allowed=date.today(),
            # max_date_allowed=date(2017, 9, 19),
            initial_visible_month=date.today(),
            date=begin_dt.date()
        ),
        dcc.Input(
            id={
                'type': 'begin_time',
                'index': clicked_point["customdata"][0]
            },
            type='time',
            value=begin_dt.time()
        ),
        html.Label(
            children = "End: ",
            className = "modal_input_label"

        ),
        dcc.DatePickerSingle(
            id={
                'type': 'end_date',
                'index': clicked_point["customdata"][0]
            },
            min_date_allowed=date.today(),
            # max_date_allowed=date(2017, 9, 19),
            initial_visible_month=date.today(),
            date=end_dt.date()
            
        ),
        dcc.Input(
            id={
                'type': 'end_time',
                'index': clicked_point["customdata"][0]
            },
            type='time',
            value=end_dt.time()
        ),
        html.Div(
            id={
                'type': 'output_container',
                'index': clicked_point["customdata"][0]
            }
        )
            # html.P([
            #     html.B('Start: {date} '.format(date=begin_dt.date())),
            #     '{time}'.format(time=begin_dt.time().strftime("%H:%M"))
            #     ]),
            # html.P([
            #     html.B('End: {date} '.format(date=end_dt.date())),
            #     '{time}'.format(time=end_dt.time().strftime("%H:%M"))
            #     ]),
    ])
    return body_text


@app.callback(
    Output('click-data', 'children'),
    Input('chart_plot', 'clickData'),
    State('df_inp', 'value'))
def display_click_data(clickData, df_inp, *args, **kwargs):
    # print(clickData)
    if clickData:
        django_dash = kwargs["request"].session.get("django_dash")
        mode = django_dash.get("mode")
        print(mode)
        clicked_point = clickData["points"][0]
        # print("clickData: ", clickData)
        jt_name = clicked_point["label"]
        begin_dt = datetime.fromisoformat(clicked_point["base"])
        end_dt = datetime.fromisoformat(clicked_point["value"])
        # during = end_dt - begin_dt
        # print(begin_dt.date(), end_dt.date())
        if mode == "defs/index":
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
            footer_text = dbc.Button("Close",
                            id={
                                'type': 'close_modal',
                                'index': clicked_point["customdata"][0]
                            }
                        )
        elif mode == "defs/job_def":
            body_text = create_form_modal_body(clicked_point)
            footer_text = html.Div([
                dbc.Button("Close",
                    id={
                        'type': 'close_modal',
                        'index': clicked_point["customdata"][0]
                    }
                ),
                dbc.Button("Submit",
                    id={
                        'type': 'submit_form',
                        'index': clicked_point["customdata"][0]
                    }
                )
            ])
        modal = html.Div([
            # dbc.Button("Open modal", id="open", n_clicks=0), 
            dbc.Modal(
                [
                    dbc.ModalHeader(
                        dbc.ModalTitle("{name}".format(name=jt_name)),
                        close_button=False),
                    dbc.ModalBody(body_text),
                    dbc.ModalFooter(footer_text),
                ],
                id="modal",
                is_open=True,
                size="xl",
                keyboard=False,
                backdrop="static",
                ),
            ])
        return modal


@app.callback(
    Output('df_inp', 'value'),
    Output("modal", "is_open"),
    Input({'type': 'close_modal', 'index': ALL}, 'n_clicks'),
    Input({'type': 'submit_form', 'index': ALL}, 'n_clicks'),
    State({'type': 'begin_date', 'index': ALL}, 'date'),
    State({'type': 'begin_time', 'index': ALL}, 'value'),
    State({'type': 'end_date', 'index': ALL}, 'date'),
    State({'type': 'end_time', 'index': ALL}, 'value'),
    State('df_inp', 'value'))
def close_modal(close_modal, submit_form, begin_date, begin_time, end_date, end_time, df_inp, *args, **kwargs):
    # print("close_modal, submit_form")
    # print(close_modal, submit_form)
    django_dash = kwargs["request"].session.get("django_dash")
    df_json = django_dash.get("df")
    # print(df_json)
    if close_modal != [None] and kwargs['callback_context'].triggered != []:
        return df_inp, False
    if submit_form != [None] and kwargs['callback_context'].triggered != []:
        context_trigger = kwargs['callback_context'].triggered[0]
        trigg_id = json.loads(context_trigger['prop_id'].split('.')[0])['index']
        df = generate_df(django_dash.get("jobtype"))
        django_index = trigg_id
        job_selected = Job.objects.get(id=int(django_index))
        # print(begin_time[0], end_date, end_time)
        setattr(job_selected, "begin_time", begin_time[0])
        setattr(job_selected, "begin_date", begin_date[0])
        setattr(job_selected, "end_time", end_time[0])
        setattr(job_selected, "end_date", end_date[0])
        # print("job_selected ", job_selected)
        job_selected.save()
#         # ujr.save()
        # df.loc[df["db_idx"] == int(trigg_id), 'begin_time'] = begin_time
        # df.loc[df["db_idx"] == int(trigg_id), 'begin_date'] = begin_date
        # df.loc[df["db_idx"] == int(trigg_id), 'end_time'] = end_time
        # df.loc[df["db_idx"] == int(trigg_id), 'end_date'] = end_date
        # print(job_selected.id)
        df = generate_df(job_selected.jobtype.id)
        df_json = df.to_json()
        django_dash['df'] = df_json
        # print("exiting alter_data, df: ", df)
        modal_show = False
        return df_json, modal_show
    print("noch nicht")
    return df_inp, True


# @app.callback(
#     Output('output_container', 'children'),
#     Input('begin_date', 'date'))
#     # Input({'type': 'submit_form', 'index': ALL}, 'n_clicks'),
# #     State({'type': 'begin_date', 'index': ALL}, 'value'),
# #     State({'type': 'begin_time', 'index': ALL}, 'value'),
# #     State({'type': 'end_date', 'index': ALL}, 'value'),
# #     State({'type': 'end_time', 'index': ALL}, 'value'),
# def update_output(date_value):
#     string_prefix = 'You have selected: '
#     if date_value is not None:
#         date_object = date.fromisoformat(date_value)
#         date_string = date_object.strftime('%B %d, %Y')
#         return string_prefix + date_string


def chart_plot(df):
    """
    Returns timeline plot.
    @param df: input df
    TODO: discrete color map and legend.
    """
    df["default_rating"] = df["default_rating"].astype(str)
    rating_color_map = {
        1: "green",
        2: "yellow",
        3: "orange",
        4: "goldenrod",
        5: "red"
        }
    rating_color_map = {str(i): rating_color_map[i] for i in rating_color_map}
    df_colors = list(OrderedDict.fromkeys(df["default_rating"]))
    plotly_colors = [rating_color_map[c] for c in df_colors]
    print(plotly_colors)
    sorted_jobtype_names = list(df["name"])
    sorted_jobtype_names.sort()
    tl = px.timeline(
        df,
        x_start="begin",
        x_end="end",
        y="name",
        color="default_rating",
        opacity=0.5,
        labels={},
        category_orders={
            "default_rating": rating_color_map.keys(),
            "name": sorted_jobtype_names
            },
        color_discrete_map=rating_color_map,
        custom_data=["job", "default_rating"]
        )
    tl.update_traces(marker_line_color='rgb(0,0,0)', marker_line_width=3, opacity=1)
    # tl.update_yaxes(autorange="reversed")
    return tl

def generate_df(jobtype_pk):
    jobtype = Jobtype.objects.get(id=jobtype_pk)
    l = []
    for j in jobtype.job_set.all():
        d = j.as_dict()
        d["job"] = j.pk
        d["db_idx"] = j.id
        d.update(jobtype.as_dict())
        l.append(d)
    df = pd.DataFrame(l)
    df['begin'] = pd.to_datetime(df['begin_date'].astype(str) + ' ' + df['begin_time'].astype(str))
    df['end'] = pd.to_datetime(df['end_date'].astype(str) + ' ' + df['end_time'].astype(str))
    df['begin'] = df['begin'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['end'] = df['end'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df