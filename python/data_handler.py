import db_connect as db
from day import Day
from jobtype import Jobtype



from datetime import datetime
import pandas as pd
import logging

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

        elif self.group == "helper":
            self.jts = pd.DataFrame(db.fetch_jobtypes(group="helper"))
            self.jobs = pd.DataFrame(db.fetch_jobs_by_group(True))
            self.users = pd.DataFrame(db.fetch_helpers())
            self.names = pd.DataFrame(db.fetch_names(helper=True))
            self.preferences = pd.DataFrame(db.fetch_preferences_by_group("helper"))

        self.days.set_index("id", inplace=True)
        self.jts.set_index("id", inplace=True)
        # self.jobs.set_index("id", inplace=True)
        # self.users.set_index("id", inplace=True)
        self.names.set_index("id", inplace=True)
        self.preferences.set_index("name_id", inplace=True)
        # print(self.all_preferences.index)
        logging.info("Data Handler initialized.")

        # print(self.preferences)


    def find_conflicts(self, br):
        """Finds conflicting jobs for each job.
        Returns dictionary {job_id: <DataFrame of conflicting jobs>}.
        @param br: individual minimum break between two shifts."""
        conflicts = {}
        # print(self.jobs)
        for id, s, e in self.jobs[["abs_start", "abs_end"]].itertuples(index=True):
            # print(id)
            tmp = self.jobs.loc[((self.jobs["abs_start"] >= s-br) & (self.jobs["abs_start"] < e+br)) | ((self.jobs["abs_end"] >= s-br) & (self.jobs["abs_end"] <= e+br))]
            conflicts[id] = tmp
            # conflicts.update(id=tmp)
            # print(self.jobs.loc[((self.jobs["abs_start"] >= s) & (self.jobs["abs_start"] < e)) | ((self.jobs["abs_end"] >= s) & (self.jobs["abs_end"] <= e))]["id"])
        # print(conflicts)
        # conflicts = pd.DataFrame(conflicts.items(), columns=["jobid", "conflicting_job_ids"])
        # print(conflicts.tail())
        # conflicts.set_index("jobid")
        # assert 1==0
        return conflicts

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
