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
from .models import UserJobRating
from django.db.models import Q

import logging
from utils.logFormatter import LogFormatter


RATES = list(map(str, range(1, 6)))

styles = {
    'app':{
        'height': '100%',
        'width': '100%',
        'overflowX': 'show',
        'overflowY': 'show'
        }
    }
app = DjangoDash('thechart', add_bootstrap_links=True)
app.layout = html.Div([
    dcc.Input(id='df_inp', type="hidden", style={"display": "hidden"}),
    dcc.Store(id="cache", data=[]),
    html.H1("Preferences", style={"text-align": "center"}),
    html.Div([
            dcc.Markdown("""
                **Click Data**
                Click on points in the graph.
            """),
            html.Pre(id='click-data', children=[]),
    ], className='three columns'),
    html.Br(),
    dcc.Graph(id="chart_plot")
    
], style=styles['app']
)


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
    fig.update_layout()
    return fig

@app.callback(
    Output('click-data', 'children'),
    Input('chart_plot', 'clickData'),
    State('df_inp', 'value'))
def display_click_data(clickData, df_inp):
    logging.debug(f"clickData: {clickData}")
    if clickData:
        clicked_point = clickData["points"][0]
        logging.debug(f"clicked_point: {clicked_point}")
        jt_name = clicked_point["label"]
        begin_dt = datetime.fromisoformat(clicked_point["base"])
        end_dt = datetime.fromisoformat(clicked_point["value"])
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
        pref_inp = html.Div([
            body_text,
            dcc.Dropdown(
                id={
                    'type': 'pref_inp',
                    'index': clicked_point["pointIndex"]
                },
                options=[
                    {'label': i, 'value': i} for i in RATES
                ],
                multi=False,
                # value=clicked_point["marker.color"],
                value=clicked_point["customdata"][1],
                clearable=False,
                style={'width': '49%', "position": "relative"},
                maxHeight=500,
                className="dropdown_row"
            )
        ], style={'display': 'inline', "height": "80%"})
        # print(clicked_point, 10*'_')
        modal = html.Div(
            [
                # dbc.Button("Open modal", id="open", n_clicks=0), 
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            dbc.ModalTitle("Rate {name}".format(name=jt_name)),
                            close_button=False),
                        dbc.ModalBody(pref_inp),
                        dbc.ModalFooter(
                            dbc.Button("Submit",
                                id={
                                    'type': 'pref_inp_btn',
                                    'index': clicked_point["customdata"][0]
                                }
                            )
                        ),
                    ],
                    id="modal",
                    is_open=True,
                    keyboard=False,
            backdrop=True,
                ),
            ]
        )
        return modal




@app.callback(
    Output('df_inp', 'value'),
    Output("modal", "is_open"),
    Input({'type': 'pref_inp_btn', 'index': ALL}, 'n_clicks'),
    State({'type': 'pref_inp', 'index': ALL}, 'value'),
    State('df_inp', 'value'))
def alter_data(pref_inp_btn, pref_inp, df_inp, *args, **kwargs):
    django_dash = kwargs["request"].session.get("django_dash")
    logging.debug(f"pref_inp_btn: {pref_inp_btn}")
    if pref_inp_btn != [None] and kwargs['callback_context'].triggered != []:
        pref = int(pref_inp[0])
        logging.info(f"pref_inp: {pref_inp}")
        logging.debug(f"pref: {pref}")
        current_user = kwargs['user']
        context_trigger = kwargs['callback_context'].triggered[0]
        trigg_id = json.loads(context_trigger['prop_id'].split('.')[0])['index']
        logging.debug(f"trigg_id: {trigg_id}")
        df = generate_df(current_user)
        # django_index = df.loc[df.index == int(trigg_id), 'job']
        django_index = trigg_id
        job_selected = Job.objects.get(id=int(django_index))
        logging.debug(f"job_selected: {job_selected}")
        # job_selected = Job.objects.all()[int(trigg_id)]
        # user_job_rating = UserJobRating.objects.filter(user=current_user).values()
        try:
            ujr = UserJobRating.objects.get(job=job_selected, user=current_user)
        except UserJobRating.DoesNotExist:
            ujr = UserJobRating(job=job_selected, user=current_user, rating=pref)
            logging.debug("New UserJobRating instance.")
        setattr(ujr, "rating", pref)
        logging.debug(f"ujr: {ujr}")
        ujr.save()
        df = generate_df(current_user)
        df_json = df.to_json()
        django_dash['df'] = df_json
        # logging.debug(f"exiting alter_data, df:\n{df}")
        modal_show = False
        return df_json, modal_show
    logging.debug("noch nicht")
    return df_inp, True
    

def chart_plot(df):
    """
    Returns timeline plot.
    @param df: input df
    TODO: discrete color map and legend.
    """
    df["rating"] = df["rating"].astype(str)
    # df_rat = df["rating"]
    # logging.debug(f"\n{df_rat.dtypes}")
    rating_color_map = {
        1: "green",
        2: "yellow",
        3: "orange",
        4: "goldenrod",
        5: "red"
        }
    rating_color_map = {str(i): rating_color_map[i] for i in rating_color_map}
    sorted_jobtype_names = list(df["name"])
    sorted_jobtype_names.sort()
    tl = px.timeline(
        df,
        x_start="begin",
        x_end="end",
        y="name",
        color="rating",
        opacity=0.5,
        labels={},
        category_orders={
            "rating": rating_color_map.keys(),
            "name": sorted_jobtype_names
            },
        color_discrete_map=rating_color_map,
        custom_data=["job", "rating"]
    )
    tl.update_traces(marker_line_color='rgb(0,0,0)', marker_line_width=3, opacity=1)
    # tl.update_yaxes(autorange="reversed")
    return tl


def generate_df(user):
    current_user = user
    jobtypes = Jobtype.objects.all()
    jobs_allowed = []
    for jt in jobtypes:
        if jt.subcrew:
            if not current_user in jt.subcrew.members.all():
                continue
        # print(jt.job_set.all().values_list("pk", flat=True))
        jobs_allowed.extend(jt.job_set.all())
    ok_job_qs = Q()
    for job_pk in jobs_allowed:
        ok_job_qs = ok_job_qs | Q(job=job_pk, user=current_user)
    user_ratings = UserJobRating.objects.filter(ok_job_qs)
    l = []
    for ur in user_ratings:
        d = ur.as_dict()
        job = ur.job.as_dict()
        job["db_idx"] = ur.job.id
        jobtype = ur.job.jobtype.as_dict()
        d.update(job)
        d.update(jobtype)
        l.append(d)
    df = pd.DataFrame(l)
    df['begin'] = pd.to_datetime(df['begin_date'].astype(str) + ' ' + df['begin_time'].astype(str))
    df['end'] = pd.to_datetime(df['end_date'].astype(str) + ' ' + df['end_time'].astype(str))
    df['begin'] = df['begin'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['end'] = df['end'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df