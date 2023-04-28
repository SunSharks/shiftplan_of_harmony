import json
import pandas as pd
from dash import dcc, html, ctx, MATCH, ALL
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.offline import plot
import chart_studio.plotly as py
import chart_studio
chart_studio.tools.set_config_file(world_readable=False, sharing='private')
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from django_plotly_dash import DjangoDash

from django.contrib.auth.models import User
from defs.models import Shiftplan, Jobtype, Job
from .models import UserJobRating
from django.db.models import Q

from .config import rating_color_map

def generate_legend():
    legend_items = []
    for rating, color in rating_color_map.items():
        legend_items.append(
            go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color=color), showlegend=True, name=f"{rating}")
        )
    legend_fig = go.Figure(legend_items)

    # Add a title to the custom legend
    legend_fig.update_layout(title="Rates")
    # legend_fig.show()
    return legend_fig

RATES = range(1, 6)
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
    dcc.Input(id='df_inp'),
    dcc.Store(id="cache", data=[]),
    html.H1("Preferences", style={"text-align": "center"}),
    # html.Div(
    #     dcc.Graph(
    #         id="the_legend",
    #         figure=generate_legend()
    #     )
    # ),
    html.Div([
            dcc.Markdown("""
                **Click Data**
                Click on points in the graph.
            """),
            html.Pre(id='click-data', children=[]),
    ], className='three columns'),
    html.Br(),
    dcc.Graph(id="chart_plot"),
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
        # print("df_inp none")
    else:
        df = pd.read_json(df_inp)
        df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
        df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    # print("generae_graph", df)
    dff = df.copy()
    fig = chart_plot(dff)
    fig.update_layout(clickmode='event+select')
    # fig.show()
    return fig

@app.callback(
    Output('click-data', 'children'),
    Input('chart_plot', 'clickData'),
    State('df_inp', 'value'))
def display_click_data(clickData, df_inp):
    if clickData:
        clicked_point = clickData["points"][0]
        print("clickData: ", clickData)
        pref_inp = html.Div([
            html.P(),
            dcc.Dropdown(
                id={
                    'type': 'pref_inp',
                    'index': clicked_point["pointIndex"]
                },
                options=[
                    {'label': i, 'value': i} for i in RATES
                ],
                multi=False,
                clearable=False,
                style={'width': '49%', "position": "relative"},
                maxHeight=500,
                className="dropdown_row"
            )
        ], style={'display': 'inline', "height": "80%"})
        modal = html.Div(
            [
                # dbc.Button("Open modal", id="open", n_clicks=0), 
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle('Rate job: {name}'.format(name=clicked_point["label"]))),
                        dbc.ModalBody(pref_inp),
                        dbc.ModalFooter(
                            dbc.Button("Submit",
                                id={
                                    'type': 'pref_inp_btn',
                                    'index': clicked_point["pointIndex"]
                                }
                            )
                        ),
                    ],
                    id="modal",
                    is_open=True,
                ),
            ]
        )
        
        # return json.dumps(clickData, indent=2)
        return modal

# @app.callback(
#     Output("modal", "is_open"),
#     [Input("open", "n_clicks"), Input("close", "n_clicks")],
#     [State("modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open


@app.callback(
    Output('df_inp', 'value'),
    Output("modal", "is_open"),
    Input({'type': 'pref_inp_btn', 'index': ALL}, 'n_clicks'),
    State({'type': 'pref_inp', 'index': ALL}, 'value'))
def alter_data(pref_inp_btn, pref_inp, *args, **kwargs):
    django_dash = kwargs["request"].session.get("django_dash")
    shiftplan_pk = kwargs["request"].session.get("shiftplan_pk")
    if pref_inp != [None] and kwargs['callback_context'].triggered != []:
        pref = int(pref_inp[0])
        current_user = kwargs['user']
        context_trigger = kwargs['callback_context'].triggered[0]
        trigg_id = json.loads(context_trigger['prop_id'].split('.')[0])['index']
        df = generate_df(current_user, shiftplan_pk)
        django_index = df.loc[df.index == int(trigg_id), 'db_idx']
        job_selected = Job.objects.get(id=int(django_index))
        # job_selected = Job.objects.all()[int(trigg_id)]
        
        # user_job_rating = UserJobRating.objects.filter(user=current_user).values()
        # print(user_job_rating)
        try:
            ujr = UserJobRating.objects.get(job=job_selected, user=current_user)
        except UserJobRating.DoesNotExist:
            ujr = UserJobRating(job=job_selected, user=current_user, rating=int(pref))
            # print("New UserJobRating instance.")
        setattr(ujr, "rating", pref)
        # print("ujr ", ujr)
        ujr.save()
        # df.loc[df["db_idx"] == int(trigg_id), 'rating'] = pref
        df = generate_df(current_user, shiftplan_pk)
        df_json = df.to_json()
        django_dash['df'] = df_json
        print("exiting alter_data, df: ", df)
        modal_show = False
        return df_json, modal_show
    

def chart_plot(df):
    # print(df)
    df["rating"] = df["rating"].astype(str)
    from .config import rating_color_map
    rating_color_map = {str(i): rating_color_map[i] for i in rating_color_map}
    tl = px.timeline(
        df, x_start="begin", x_end="end", y="name", color="rating", opacity=0.5, labels={}, color_discrete_map=rating_color_map)
    tl.update_traces(marker_line_color='rgb(0,0,0)', marker_line_width=3, opacity=1)
    tl.update_yaxes(autorange="reversed")
    return tl


def generate_df(user, sp_pk):
    current_user = user
    shiftplan = Shiftplan.objects.get(pk=sp_pk)
    jobtypes = shiftplan.jobtype_set.all()
    jobs_allowed = []
    for jt in jobtypes:
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