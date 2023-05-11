
# ./manage.py dumpdata > db.json
# python manage.py dumpdata defs > ../python/django_to_2022_translate/db.json

# import mysql.connector
import pandas as pd
import json
from os.path import join
from get_db_json import models_names, paths



shiftplan_name = "Crew"
# build_tables_structure(("db.json")

def build_tables_structure():
    models = {}
    for fn in models_names:
        with open(join(paths["json_out"], fn+".json"), 'r') as f:
            models.update({fn: pd.json_normalize(json.loads(f.read()))})
    # print(models)
    for m in models:
        models[m] = models[m].rename(columns={old: old.replace("fields.", "", 1).lstrip() for old in models[m].columns})
    return models
# df = df.drop(df[<some boolean condition>].index)

def make_jobs():
    pass



if __name__ == "__main__":
    models = build_tables_structure()
    jobtypes = models["jobtypes"]
    print(jobtypes)
    models["jobs"]["begin"] = pd.to_datetime(models["jobs"]['begin_date'] + ' ' + models["jobs"]['begin_time'])
    models["jobs"]["end"] = pd.to_datetime(models["jobs"]['end_date'] + ' ' + models["jobs"]['end_time'])
    models["jobs"]["during"] = models["jobs"]["end"] - models["jobs"]["begin"]
    print(models["user_profiles"])
    workers = models["user_profiles"].loc[models["user_profiles"]["worker"] == True]
    print(workers) 
