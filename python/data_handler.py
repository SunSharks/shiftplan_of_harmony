import db_connect as db


from datetime import datetime
import pandas as pd
import logging
import numpy as np

try:
    from colorama import init
    init()
except ImportError:
    pass

# from helper.logFormatter import LogFormatter

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# ch.setFormatter(LogFormatter())
logger.addHandler(ch)


class Data_Handler:
    def __init__(self, group="crew", name=""):
        self.group = group
        self.days = pd.DataFrame(db.fetch_days())

        if self.group == "crew":
            self.jts = pd.DataFrame(db.fetch_jobtypes(group="crew"))
            self.jobs = pd.DataFrame(db.fetch_jobs_by_group(False))
            self.users = pd.DataFrame(db.fetch_users())
            self.names = pd.DataFrame(db.fetch_names(helper=False))
            self.preferences = pd.DataFrame(db.fetch_preferences_by_group("user"))
            self.exclusives = pd.DataFrame(db.fetch_exclusives())

        elif self.group == "helper":
            self.jts = pd.DataFrame(db.fetch_jobtypes(group="helper"))
            self.jobs = pd.DataFrame(db.fetch_jobs_by_group(True))
            self.users = pd.DataFrame(db.fetch_helpers())
            self.names = pd.DataFrame(db.fetch_names(helper=True))
            self.preferences = pd.DataFrame(db.fetch_preferences_by_group("helper"))

        self.days.set_index("id", inplace=True)
        self.jts.set_index("id", inplace=True)
        self.names.set_index("id", inplace=True)
        # print(self.preferences)
        self.preferences.set_index("name_id", inplace=True)
        self.names_to_users()
        logging.info("Data Handler initialized.")
        # print(len(self.preferences.index))

        # print(self.preferences)

    def names_to_users(self):
        sensible_jts = self.jts.loc[self.jts["special"] == 1].index
        unsensible_jts = self.jts.loc[self.jts["special"] == 0].index
        sensible_jobs = self.jobs.loc[self.jobs["jt_primary"].isin(sensible_jts)].index
        unsensible_jobs = self.jobs.loc[self.jobs["jt_primary"].isin(unsensible_jts)].index
        default_preferences = np.empty(len(self.jobs.index))
        default_preferences[sensible_jobs] = 5
        default_preferences[unsensible_jobs] = 3

        unregistered_names = self.names.loc[~self.names.index.isin(
            self.users["fullname_id"])]
        print(unregistered_names)
        for id, sn, fn in unregistered_names[["surname", "famname"]].itertuples(index=True):
            self.users = self.users.append(
                {'fullname_id': id, 'nickname': sn+fn, 'break': 4, 'bias': 0}, ignore_index=True)
            # prefs = []
            default_row = {}
            for i, c in enumerate(self.preferences):
                if c == "name_id":
                    default_row["name_id"] = id
                    continue
                default_row[c] = default_preferences[i]
            df = pd.DataFrame(default_row, index=[id])
            # print(df.shape)
            self.preferences = pd.concat([self.preferences, df])
        print(self.preferences.index)
        no_preferences = self.names.loc[~self.names.index.isin(self.preferences.index)].index
        for id in no_preferences:
            # default_row["name_id"] = id
            df = pd.DataFrame(default_row, index=[id])
            self.preferences = pd.concat([self.preferences, df])

    def is_neighbor(j1_end, j2_start):
        return j1_end == j2_start

    def tester(self):
        # print(self.conflicts.loc[self.conflicts["jobid"] ==4])
        approved = True
        # self.jobs.set_index("id")
        for jobid, confs in self.conflicts[["jobid", "conflicting_job_ids"]].itertuples(index=False):
            # print(jobid in self.jobs.values)
            if not jobid in self.jobs.values:
                # print(jobid)
                approved = False
            for c in confs:
                # print(c in self.jobs.values)
                if not c in self.jobs.values:
                    # print(c)
                    approved = False

        print(50*"-")
        print(approved)

        #


if __name__ == "__main__":
    handler = Data_Handler()
    handler.tester()
