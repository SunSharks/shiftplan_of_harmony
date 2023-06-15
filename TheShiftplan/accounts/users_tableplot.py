import logging
import base64
import io
import csv
import pandas as pd
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

from .models import UserCandidate

from utils import config

app = DjangoDash('users_tableplot', add_bootstrap_links=True)

app.layout = html.Div([
    html.P(id='placeholder'),
    dcc.Upload(
        id='datatable-upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
        },
    ),
    dash_table.DataTable(
        id='adding-rows-table',
        columns=[{
            'name': col,
            'id': col,
            'deletable': False,
            'renamable': False
        } for col in config.code_to_file_dict.keys()
        ],
        # data=[],
        editable=True,
        row_deletable=True
    ),
    html.Button('Add Row', id='add-row-button', n_clicks=0),
    html.Button('Submit', id='submit-table', n_clicks=0),
])


@app.callback(
    Output('adding-rows-table', 'data'),
    Input('add-row-button', 'n_clicks'),
    Input('datatable-upload', 'contents'),
    State('adding-rows-table', 'data'),
    State('adding-rows-table', 'columns'),
    State('datatable-upload', 'filename'))
def execute(n_clicks, contents, rows, columns, filename, *args, **kwargs):
    django_dash = kwargs["request"].session.get("django_dash")
    if rows is None:
        user_cands = django_dash.get('user_candidates')
        rows = user_cands
    if not contents is None:
        new_df = parse_contents(contents, filename)
        new_df = rename_columns(new_df)
        rows_df = pd.DataFrame(rows)
        df = join_dfs(rows_df, new_df)
        logging.debug(df)
        rows = df.to_dict(orient='records')
        django_dash["new_df"] = new_df.to_dict(orient='records')
    
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@app.callback(
    Output('placeholder', 'children'),
    Input('submit-table', 'n_clicks'),
    State('adding-rows-table', 'data'))
def alter_data(n_clicks, rows, *args, **kwargs):
    drop_none_vals = lambda d: {key: val for key, val in d.items() if not val is None}
    django_dash = kwargs["request"].session.get("django_dash")
    if rows is None:
        user_cands = django_dash.get('user_candidates')
        rows = user_cands
    if n_clicks > 0:
        for row in rows:
            r = {key: row.get(key) for key in row if key in config.unique_together}
            non_unique = {key: row.get(key) for key in row if not key in config.unique_together}
            r = drop_none_vals(r)
            non_unique = drop_none_vals(non_unique)
            try:
                user_cand = UserCandidate.objects.get(**r)
                inst_dict = user_cand.as_dict()
                for key, val in non_unique.items():
                    if inst_dict[key] != val:
                        setattr(user_cand, key, val)
                        user_cand.save()
                        logging.debug("Saved new {key}: {val}")
                        logging.debug(user_cand)
            except UserCandidate.DoesNotExist:
                user_cand = UserCandidate(**row)
                user_cand.save()
            
    return None


def join_dfs(old_df, new_df):
    """Join DataFrames (rows)."""
    # Identify common columns
    common_columns = set(old_df.columns) & set(new_df.columns) - set(config.unique_together)
    for col in old_df.columns:
        if col not in new_df.columns:
            new_df[col] = None
    # Append new records from the new DataFrame to the old DataFrame
    df = old_df.append(new_df, ignore_index=True)
    # Remove duplicate entries based on unique-together columns in old_df
    df.drop_duplicates(subset=config.unique_together, keep='last', inplace=True)
    return df


def rename_columns(df):
    """
    Renames df columns according to config.code_to_file_dict.
    @param df: pd.DataFrame
    Returns DataFrame with renamed columns.
    """
    renames = {}
    for c in df.columns:
        if c.lower() in config.file_to_code_dict:
            renames[c] = config.file_to_code_dict[c.lower()]
    df = df.rename(columns=renames)
    df = df[renames.values()]
    return df


# def create_candidate_instances(file, df):
#     print(df)
#     fname = file.name.split(".")[0]
#     conflicting = CandidatesList.objects.filter(name=fname)
#     conflicting.delete()
#     cand_list = CandidatesList(name=fname, file=file)
#     cand_list.save()
    
#     for i in df.index:
#         user_cand = UserCandidate()
#         for attr_name in renames.values():
#             setattr(user_cand, attr_name, df.iloc[i][attr_name])
#         setattr(user_cand, "candidates_list", cand_list)
#         print(user_cand)
#         user_cand.save()


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if filename.endswith(".csv"):
        # Assume that the user uploaded a CSV file
        io_str = io.StringIO(decoded.decode('utf-8'))
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(io_str.read()).delimiter
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')),
            delimiter=delimiter
            )
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


if __name__ == '__main__':
    app.run_server(debug=True)