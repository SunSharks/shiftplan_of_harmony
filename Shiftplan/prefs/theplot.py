import json
import pandas as pd
from dash import dcc, html, ctx, MATCH, ALL
from dash.dependencies import Input, Output

import plotly.express as px
from plotly.offline import plot
import chart_studio.plotly as py
import chart_studio
chart_studio.tools.set_config_file(world_readable=False, sharing='private')
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash

from django.contrib.auth.models import User
from defs.models import Shiftplan, Jobtype, Job
from .models import UserJobRating

RATES = range(1, 6)
styles = {
    'app':{
        'height': '100%',
        'width': '100%',
        'overflowX': 'show',
        'overflowY': 'show'
        }
    }
app = DjangoDash('thechart')
app.layout = html.Div([
    dcc.Input(id='df_inp'),
    html.H1("Preferences", style={"text-align": "center"}),
    html.Div(className='row', children=[
        html.Div([
                dcc.Markdown("""
                    **Click Data**

                    Click on points in the graph.
                """),
                html.Pre(id='click-data', children=[]),
        ], className='three columns', style=styles['app']),
        html.Br()
        ], style=styles['app']
    ),
    dcc.Graph(id="chart_plot")
], style=styles['app'])


@app.callback(
    Output('chart_plot', 'figure'),
    [Input('df_inp', 'value')])
def generate_graph(df_inp, *args, **kwargs):
    # print(args)
    print(15*"-"+"generae_graph")
    # print(kwargs)
    # print(kwargs["request"].session.get("django_dash"))
    if df_inp is None:
        django_dash = kwargs["request"].session.get("django_dash")
        df = pd.read_json(django_dash.get('df'))
        df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
        df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
        print("df_inp none")
    else:
        df = pd.read_json(df_inp)
        df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
        df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
        print("df_inp NOT none")
    # user = kwargs['user']    
    print(df)
    dff = df.copy()
    fig = chart_plot(dff)
    fig.update_layout(clickmode='event+select')
    # fig.show()
    return fig

@app.callback(
    Output('click-data', 'children'),
    Input('chart_plot', 'clickData'))
def display_click_data(clickData):
    if clickData:
        pref_inp = html.Div([
            
            dcc.Dropdown(
                id={
                    'type': 'pref_inp',
                    'index': clickData["points"][0]["pointIndex"]
                },
                options=[
                    {'label': i, 'value': i}for i in RATES
                ],
                multi=False,
                value=3
            )
        ])
        # return json.dumps(clickData, indent=2)
        return pref_inp


@app.callback(
    Output('df_inp', 'value'),
    Input({'type': 'pref_inp', 'index': ALL}, 'value'))
def alter_data(pref_inp, *args, **kwargs):
    try:
        print(kwargs['callback_context'].triggered)
        print("juuuu")
    except LookupError:
        print("ERROR")
    # print(help(ctx))
    # ctx_msg = json.dumps({
    #     'states': ctx.states,
    #     'triggered': ctx.triggered,
    #     'inputs': ctx.inputs
    # }, indent=2)
    # # print(ctx_msg)
    # print(ctx.get('triggered_id'))
    # button_id = ctx.triggered_id if not None else 'No clicks yet'
    print(10*'_'+'\n')
    # print(ctx.triggered_id)
    # print(button_id)
    if pref_inp and kwargs['callback_context'].triggered != []:
        context_trigger = kwargs['callback_context'].triggered[0]
        print(context_trigger['prop_id'])
        print(json.loads(context_trigger['prop_id'].split('.')[0]))
        trigg_id = json.loads(context_trigger['prop_id'].split('.')[0])['index']
        print(trigg_id)
        pref = context_trigger['value']
        print(pref)
        print(type(pref))
        job_selected = trigg_id
        # print(job_selected)
        # print(kwargs)
        django_dash = kwargs["request"].session.get("django_dash")
        print(django_dash)
        df = pd.read_json(django_dash.get('df'))
        print(df.iloc[2]["rating"])
        df.loc[df.index == trigg_id, 'rating'] = pref
        print(df["rating"].iloc[2])
        # kwargs["request"].session.get("django_dash").get("df").set(df.to_json())
        # df_json = django_dash.get('df')
        # print(df_json)
        df_json = df.to_json()
        return df_json
    

def chart_plot(df):
    print(df['begin'])
    print(df['end'])
    print(df['name'])
    tl = px.timeline(
        df, x_start="begin", x_end="end", y="name", color="rating", opacity=0.5)
    # fig = px.bar(df, x='during', y='name', color='name')
    tl.update_yaxes(autorange="reversed")
    # fig['layout']['xaxis'].update({'type': None})
    # fig.update_xaxes(type='category')
    # gantt_plot = plot(fig)#, output_type="div")
    # tl.update_traces()
    print(tl.data)
    return tl
# @app.callback(
#     Output(component_id="chart_plot", component_property="figure"),
#     [Input(component_id="job_pref_input", component_property="value")]
# )
# def update_graph(pref_selected, session_state=None, **kwargs):
#     print(pref_selected)
#     print(type(pref_selected))
#     if session_state is None:
#         raise NotImplementedError("Cannot handle a missing session state")
#     df = session_state.get('df')
#     print(df)
#     dff = df.copy()
#     dff.loc['rating'] = pref_selected

    
#     # fig.update_traces(marker_size=20)
#     return fig
