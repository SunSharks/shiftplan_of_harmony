import mysql.connector

try:
    from _config import config
except:
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'Testplan',
        'raise_on_warnings': True
    }


def fetch_all(sql, result_struct="dict"):
    cnx = mysql.connector.connect(**config)
    if result_struct == "dict":
        cur = cnx.cursor(dictionary=True)
    else:
        cur = cnx.cursor()
    cur.execute(sql)

    # Fetch one result
    row = cur.fetchall()
    cnx.close()
    return row


def fetch_one(sql, result_struct="dict"):
    cnx = mysql.connector.connect(**config)
    if result_struct == "dict":
        cur = cnx.cursor(dictionary=True)
    else:
        cur = cnx.cursor()
    cur.execute(sql)
    # Fetch one result
    row = cur.fetchone()
    cnx.close()
    return row


def fetch_days():
    sql = """ SELECT id,
    name,
    date
    FROM Days"""
    return fetch_all(sql)


def fetch_jobtypes(group="all"):
    sql = """ SELECT id,
    name,
    competences,
    special,
    helper,
    name_appendix
    FROM Jobtypes"""
    if group == "helper":
        sql += " WHERE helper = 1"
    elif group == "crew":
        sql += " WHERE helper = 0"
    sql += " ORDER BY name"
    return fetch_all(sql)


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
    print(50*"_")
    print(fetch_preferences(9))
    print(fetch_all("SELECT id FROM Names WHERE registered = 1"))
