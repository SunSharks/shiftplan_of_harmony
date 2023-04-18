
# ./manage.py dumpdata > db.json
# python manage.py dumpdata defs > ../python/django_to_2022_translate/db.json

# import mysql.connector
import pandas as pd
import json

from get_db_json import models_names

from config import shiftplans



shiftplan_name = "Crew"
# build_tables_structure(("db.json")

def build_tables_structure():
    models = {}
    for fn in models_names:
        with open(fn+".json", 'r') as f:
            models.update({fn: pd.json_normalize(json.loads(f.read()))})
    # print(models)
    return models
# df = df.drop(df[<some boolean condition>].index)

def fetch_all(sql, result_struct="dict"):
    # cnx = mysql.connector.connect(**config)
    # if result_struct == "dict":
    #     cur = cnx.cursor(dictionary=True)
    # else:
    #     cur = cnx.cursor()
    # cur.execute(sql)

    # # Fetch one result
    # row = cur.fetchall()
    # cnx.close()
    row = None
    return row


def fetch_one(sql, result_struct="dict"):
    # cnx = mysql.connector.connect(**config)
    # if result_struct == "dict":
    #     cur = cnx.cursor(dictionary=True)
    # else:
    #     cur = cnx.cursor()
    # cur.execute(sql)
    # # Fetch one result
    # row = cur.fetchone()
    # cnx.close()
    row = None
    return row


def fetch_days():
    sql = """ SELECT id,
    name,
    date
    FROM Days"""
    days = {}
    return fetch_all(sql)


def fetch_jobtypes(shiftplan_pk):
    jts = models["jobtypes"].loc[
            models["jobtypes"]["fields.shiftplan"] == shiftplan_pk]
    # print(jts)
    sql = """ SELECT id,
    name,
    competences,
    special,
    helper,
    name_appendix
    FROM Jobtypes"""
    jts = jts.loc[jts["fields.shiftplan"] == group]
    for c in jts.columns:
        print(c)
    return jts


def fetch_jobs():
    sql = """ SELECT id,
    abs_start,
    abs_end,
    during,
    start_day_id,
    end_day_id,
    dt_start,
    dt_end,
    jt_primary
    FROM Jobs"""
    return fetch_all(sql)


def fetch_jobs_by_group(helper):
    sql = """ SELECT id,
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
    )""".format(int(helper))
    return fetch_all(sql)


def fetch_names(helper=False):
    sql = """ SELECT id,
    surname,
    famname,
    registered
    FROM Names"""
    if not helper == "all":
        sql += """ WHERE helper = {}""".format(int(helper))
    return fetch_all(sql)


def fetch_users():
    sql = """ SELECT id,
    fullname_id,
    nickname,
    email,
    break,
    bias
    FROM Users"""
    return fetch_all(sql)


def fetch_helpers():
    sql = """ SELECT id,
    fullname_id,
    nickname,
    email,
    break,
    workload
    FROM Helpers"""
    return fetch_all(sql)


def fetch_preferences(name_id):
    jobnames = fetch_column_names("Preferences", addon=" AND  COLUMN_NAME LIKE 'job%'")
    sql = "SELECT "
    for jn in jobnames:
        # print(jn[0])
        sql += jn[0] + ", "
    sql = sql.rstrip()[:-1]
    sql += " FROM Preferences WHERE name_id = {}".format(name_id)
    # print(sql)
    return fetch_one(sql)


def fetch_job_ids_by_group(helper):
    sql = """ SELECT id
    FROM Jobs WHERE jt_primary IN(
    SELECT id from Jobtypes WHERE helper = {}
    )""".format(int(helper))
    return fetch_all(sql)


def fetch_preferences_by_group(group):
    if group == "user":
        group_job_ids = fetch_job_ids_by_group(False)
    elif group == "helper":
        group_job_ids = fetch_job_ids_by_group(True)
    colnamesstr = ""
    for d in group_job_ids:
        colnamesstr += "job{},".format(d["id"])
    colnamesstr = colnamesstr[:-1]
    jobnames = fetch_column_names("Preferences", addon="")
    sql = "SELECT name_id, {colnames} FROM Preferences WHERE name_id IN ".format(
        colnames=colnamesstr)
    if group == "user":
        sql += "(SELECT id FROM Names WHERE Names.helper=0);"
    elif group == "helper":
        sql += "(SELECT id FROM Names WHERE Names.helper=1);"
    # print(sql)
    return fetch_all(sql)


def fetch_all_preferences():
    jobnames = fetch_column_names("Preferences", addon="")
    sql = "SELECT "
    for jn in jobnames:
        sql += jn + ", "
    # assert 1==0
    sql = sql.rstrip()[:-1]
    sql += " FROM Preferences"
    # print(sql)
    return fetch_all(sql)


def fetch_exclusives():
    sql = "SELECT jt_name, fullname_id FROM Exclusives;"
    # print(sql)
    return fetch_all(sql)


def fetch_column_names(tablename, addon=""):
    sql = """SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME= '{}' {}""".format(tablename, addon)
    ret = fetch_all(sql, "lst")
    # print([i[0] for i in ret])
    return [i[0] for i in ret]


if __name__ == "__main__":
    # print(fetch_all("SELECT * FROM Jobtypes"))
    # print(50*"_")
    # print(fetch_preferences(9))
    # print(fetch_all("SELECT id FROM Names WHERE registered = 1"))
    models = build_tables_structure()
    # fetch_jobtypes()
    for sp in shiftplans:
        # print(models["shiftplans"].loc[models["shiftplans"]["fields.name"] == sp])
        shiftplan = models["shiftplans"].loc[models["shiftplans"]["fields.name"] == sp]
        jobtypes = models["jobtypes"].loc[
            models["jobtypes"]["fields.shiftplan"] == shiftplan["pk"][0]]
        # jobtypes = fetch_jobtypes(shiftplan)
        print(jobtypes)
