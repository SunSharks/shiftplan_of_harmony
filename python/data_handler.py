import db_connect as db
from day import Day
from jobtype import Jobtype

from datetime import datetime
import pandas as pd


class Data_Handler:
    def __init__(self, name=""):
        self.days = pd.DataFrame(db.fetch_days())
        self.crew_jts = pd.DataFrame(db.fetch_jobtypes(group="crew"))
        self.helper_jts = pd.DataFrame(db.fetch_jobtypes(group="helper"))
        self.crew_jobs = pd.DataFrame(db.fetch_jobs_by_group(False))
        self.helper_jobs = pd.DataFrame(db.fetch_jobs_by_group(True))
        self.users = pd.DataFrame(db.fetch_users())
        self.crew_names = pd.DataFrame(db.fetch_names(helper=False))
        self.helper_names = pd.DataFrame(db.fetch_names(helper=True))

        self.helpers = pd.DataFrame(db.fetch_helpers())
        # print(db.fetch_all_preferences())

        self.days.set_index("id", inplace=True)
        self.crew_jts.set_index("id", inplace=True)
        self.helper_jts.set_index("id", inplace=True)
        self.crew_jobs.set_index("id", inplace=True)
        self.helper_jobs.set_index("id", inplace=True)
        self.users.set_index("id", inplace=True)
        self.crew_names.set_index("id", inplace=True)
        self.helper_names.set_index("id", inplace=True)

        print(self.crew_names.index)
        # self.crew_names.drop(42)
        self.users.drop(5)
        self.helpers.set_index("id", inplace=True)

        self.all_preferences = pd.DataFrame(db.fetch_all_preferences())
        self.all_preferences.set_index("name_id")

        self.user_preferences = pd.DataFrame(db.fetch_preferences_by_group("user"))
        self.helper_preferences = pd.DataFrame(db.fetch_preferences_by_group("helper"))
        self.user_preferences.set_index("name_id")
        self.helper_preferences.set_index("name_id")
        # print(self.all_preferences.index)
        self.find_conflicts()
        # print(self.user_preferences)


    def find_conflicts(self):
        conflicts = {}
        print(self.crew_jobs)
        for id, s, e in self.crew_jobs[["abs_start", "abs_end"]].itertuples(index=True):
            tmp = self.crew_jobs.loc[((self.crew_jobs["abs_start"] >= s) & (self.crew_jobs["abs_start"] < e)) | ((self.crew_jobs["abs_end"] >= s) & (self.crew_jobs["abs_end"] <= e))].index
            conflicts.update(id=tmp)

            # print(self.crew_jobs.loc[((self.crew_jobs["abs_start"] >= s) & (self.crew_jobs["abs_start"] < e)) | ((self.crew_jobs["abs_end"] >= s) & (self.crew_jobs["abs_end"] <= e))]["id"])
        self.conflicts = pd.DataFrame(conflicts.items(), columns=["jobid", "conflicting_job_ids"])
        self.conflicts.set_index("jobid")



    def tester(self):
        # print(self.conflicts.loc[self.conflicts["jobid"] ==4])
        approved = True
        self.crew_jobs.set_index("id")
        for jobid, confs in self.conflicts[["jobid", "conflicting_job_ids"]].itertuples(index=False):
            # print(jobid in self.crew_jobs.values)
            if not jobid in self.crew_jobs.values:
                # print(jobid)
                approved = False
            for c in confs:
                # print(c in self.crew_jobs.values)
                if not c in self.crew_jobs.values:
                    # print(c)
                    approved = False

        print(50*"-")
        print(approved)

        #

if __name__ == "__main__":
    handler = Data_Handler()
    handler.tester()
