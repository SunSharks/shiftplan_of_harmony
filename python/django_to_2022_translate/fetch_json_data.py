# ./manage.py dumpdata > db.json
# python manage.py dumpdata defs > ../python/django_to_2022_translate/db.json

import pandas as pd
import json
from os.path import join

from get_db_json import models_names

from config import shiftplans

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

def fetch_shiftplan_pk(name="Crew"):
    shiftplan = models["shiftplans"].loc[models["shiftplans"]["name"] == name]
    pk = shiftplan["pk"][0]
    return pk

def fetch_jobtypes(shiftplan_pk):
    """Translates jobtypes from django structure to old structure. 
    sql: SELECT id,
    name,
    competences,
    special,
    helper,
    name_appendix
    FROM Jobtypes"""
    jts = models["jobtypes"].loc[
            models["jobtypes"]["shiftplan"] == shiftplan_pk]
    # jts = strip_columns(jts)
    # jts.loc[:, 'special'] = 0
    # jts.loc[:, 'helper'] = 0
    # jts.loc[:, 'name_appendix'] = ""
    jts = jts.assign(special=0)
    jts = jts.assign(helper=0)
    jts = jts.assign(name_appendix="")
    jts = jts.rename(columns={'description': 'competences', 'pk': 'id'})
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
    # print(models["jobs"])
    jobs = models["jobs"]#.loc[
    #         models["jobs"]["jobtype"] in jobtype_ids]
    jobs = jobs[jobs['jobtype'].isin(jobtype_ids)]
    jobs['datetime_start'] = pd.to_datetime(jobs['begin_date'] + ' ' + jobs['begin_time'])
    jobs['datetime_end'] = pd.to_datetime(jobs['end_date'] + ' ' + jobs['end_time'])
    jobs["during"] = jobs['datetime_end'] - jobs['datetime_start']
    jobs['during'] = jobs['during'] / pd.Timedelta(hours=1)
    jobs = jobs.reset_index(drop=True)
    # print(jobs)
    return jobs

def fetch_users(shiftplan_pk):
    """ SELECT id,
    fullname_id,
    nickname,
    email,
    break,
    bias
    FROM Users"""
    shiftplan = models["shiftplans"].iloc[shiftplan_pk]
    # print(models["users"])
    shiftplan_group = shiftplan["group"]
    # print(shiftplan_group)
    users = []
    # print(models["user_options"].user)
    for user_idx in models["users"].index:
        if shiftplan_group in  models["users"].iloc[user_idx].groups:
            users.append(user_idx)
    users_df = models["users"].iloc[users]
    users_pks = list(users_df["pk"])
    all_user_options = models["user_options"]
    user_options = all_user_options[all_user_options["user"].isin(users_pks)]
    users_df = users_df.rename(columns={'pk': 'user_pk'})
    user_options = user_options.rename(columns={'user': 'user_pk'})
    # user_options.join(users_df, on=["user_pk"])
    user_options = user_options.merge(users_df[['user_pk', 'username', 'groups']], how='left').fillna("")
    user_options = user_options.rename(columns={
        'username': 'nickname',
        "min_break_hours": "break",
        "bias_hours": "bias"
        })
    # print("user_options: ", user_options)
    user_options["break"] = pd.to_timedelta(user_options["break"], unit="h", errors='raise')
    return user_options


def fetch_preferences_by_group(users, jobs):
    # print(users, jobs)
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
    for sp in shiftplans:
        # print(models["shiftplans"].loc[models["shiftplans"]["name"] == sp])
        shiftplan_pk = fetch_shiftplan_pk(sp)
        jobtypes = fetch_jobtypes(shiftplan_pk)
        # print(list(jobtypes["id"]))
        jobs = fetch_jobs(*list(jobtypes["id"]))
        # jobtypes = fetch_jobtypes(shiftplan)
        # print(jobtypes)