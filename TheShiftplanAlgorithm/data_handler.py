
import fetch_json_data as db


class Data_Handler:
    def __init__(self, name=""):
        self.jts = db.fetch_jobtypes()
        self.jobs = db.fetch_jobs(*list(self.jts["pk"]))
        self.users = db.fetch_users()
        # self.subcrews = db.fetch_names(helper=False)
        self.preferences = db.fetch_preferences(self.users, self.jobs)
        # self.exclusives = db.fetch_exclusives()

        # # print(self.jts)
        # print(self.jobs)
        # print(self.find_conflicts())
        # self.days.set_index("id", inplace=True)
        # self.jts.set_index("id", inplace=True)
        # self.names.set_index("id", inplace=True)
        # # print(self.preferences)
        # self.preferences.set_index("name_id", inplace=True)
        # self.names_to_users()
        # with open("{}_sol/days.pkl".format(self.group), 'wb') as f:
        #     pickle.dump(self.days, f)
        # with open("{}_sol/jts.pkl".format(self.group), 'wb') as f:
        #     pickle.dump(self.jts, f)
        # with open("{}_sol/jobs.pkl".format(self.group), 'wb') as f:
        #     pickle.dump(self.jobs, f)
        # with open("{}_sol/users.pkl".format(self.group), 'wb') as f:
        #     pickle.dump(self.users, f)
        # with open("{}_sol/names.pkl".format(self.group), 'wb') as f:
        #     pickle.dump(self.names, f)
        # with open("{}_sol/preferences.pkl".format(self.group), 'wb') as f:
        #     pickle.dump(self.preferences, f)
        # with open("{}_sol/exclusives.pkl".format(self.group), 'wb') as f:
        #     pickle.dump(self.exclusives, f)
        # logging.info("Data Handler initialized.")
        # self.print_job_five()

        # print(len(self.preferences.index))

        # print(self.preferences)


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
        #
        # print(50*"-")
        # print(approved)

        #
    def print_job_five(self):
        print("Nur mit 5 bewertet: ")
        print(self.preferences.loc[:, self.preferences.nunique() == 5])

    def find_conflicts(self):
        """Finds conflicting jobs for each job.
        Returns dictionary {job_id: <DataFrame of conflicting jobs>}.
        """
        conflicts = {}
        # print(self.dh.jobs)
        c = 0
        for id, s, e in self.jobs[["datetime_start", "datetime_end"]].itertuples(index=True):
            # print(id)
            tmp = self.jobs.loc[((self.jobs["datetime_start"] >= s) & (self.jobs["datetime_start"] < e))
                                   | ((self.jobs["datetime_end"] >= s) & (self.jobs["datetime_end"] <= e))]
            conflicts[c] = tmp
            c += 1
        # print(conflicts)
        return conflicts


if __name__ == "__main__":
    handler = Data_Handler()
    # handler.tester()
