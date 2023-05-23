# ./manage.py dumpdata > db.json
# python manage.py dumpdata defs > ../python/django_to_2022_translate/db.json

import pandas as pd
import json
from os.path import join

from bash_table_export import models_names


json_path = "_json"

def strip_columns(df):
    df.columns = [c.replace("fields.", "", 1) for c in df.columns]
    return df


def build_tables_structure():
    models = {}
    for fn in models_names:
        file_path = join(json_path, fn+".json")
        with open(file_path, 'r') as f:
            models.update({fn: pd.json_normalize(json.loads(f.read()))})
    for m in models:
        models[m] = strip_columns(models[m])
    # print(models)
    return models


def fetch_jobtypes():
    """Translates jobtypes from django structure to old structure. 
    sql: SELECT id,
    name,
    competences,
    special,
    helper,
    name_appendix
    FROM Jobtypes"""
    jts = models["jobtypes"]
    # jts = strip_columns(jts)
    # jts.loc[:, 'special'] = 0
    # jts.loc[:, 'helper'] = 0
    # jts.loc[:, 'name_appendix'] = ""
    jts = jts.assign(special=0)
    jts = jts.assign(helper=0)
    jts = jts.assign(name_appendix="")
    jts = jts.rename(columns={'description': 'competences'})
    # print(jts)
    return jts

def fetch_jobs(*jobtype_ids):
    """ SELECT id,
        abs_start,
        abs_end,
        during,
        start_day_id,
        end_day_id,
        dt_start,
        dt_end,
        jt_primary
        FROM Jobs WHERE jt_primary IN(
        SELECT id from Jobtypes WHERE helper = {}
        )"""
    # print(jobtype_ids)
    jobs = models["jobs"]
    jobs = jobs[jobs['jobtype'].isin(jobtype_ids)]
    jobs['datetime_start'] = pd.to_datetime(jobs['begin_date'] + ' ' + jobs['begin_time'])
    jobs['datetime_end'] = pd.to_datetime(jobs['end_date'] + ' ' + jobs['end_time'])
    jobs["during"] = jobs['datetime_end'] - jobs['datetime_start']
    jobs['during'] = jobs['during'] / pd.Timedelta(hours=1)
    jobs = jobs.reset_index(drop=True)
    # print(jobs)
    return jobs

def fetch_users():
    """ SELECT id,
    fullname_id,
    nickname,
    email,
    break,
    bias
    FROM Users"""
    users_df = models["users"]
    users_pks = list(users_df["pk"])
    all_user_options = models["user_options"]
    user_options = all_user_options[all_user_options["user"].isin(users_pks)]
    users_df = users_df.rename(columns={'pk': 'user_pk'})
    user_options = user_options.rename(columns={'user': 'user_pk'})
    bias_hours = models["bias_hours"]
    bias_hours = bias_hours.rename(columns={
        'user': 'user_pk',
        'approved': 'bias_hours_approved'
    })
    user_options = user_options.merge(users_df[['user_pk', 'username']], how='left').fillna("")
    user_options = user_options.merge(bias_hours[['user_pk', 'bias_hours', 'bias_hours_approved']], how='left').fillna("")
    user_options = user_options.rename(columns={
        'username': 'nickname',
        "min_break_hours": "break",
        "bias_hours": "bias"
        })
    # print("user_options: ", user_options)
    user_options["break"] = pd.to_timedelta(user_options["break"], unit="h", errors='raise')
    workers = models["user_profiles"].loc[models["user_profiles"]["worker"] == True]
    workers_user_pks = list(workers["user"])
    user_options = user_options[user_options["user_pk"].isin(workers_user_pks)]
    return user_options


def fetch_preferences(users, jobs):
    print(users, jobs)
    all_ujrs = models["user_job_ratings"]
    
    ujrs = all_ujrs[all_ujrs["user"].isin(list(users["user_pk"]))]
    ujrs = ujrs[ujrs["job"].isin(list(jobs["pk"]))]
    # ujrs.set_index(list(range(len(ujrs.index))))
    # print(ujrs)
    # print(jobs)
    return ujrs





models = build_tables_structure()
    # fetch_jobtypes()
if __name__ == "__main__":
    # print(models)
    jobtypes = fetch_jobtypes()
    # print(list(jobtypes["id"]))
    jobs = fetch_jobs(*list(jobtypes["pk"]))
    users = fetch_users()
    # print(jobtypes)