
import fetch_json_data as db


class Data_Handler:
    def __init__(self, group="crew", name=""):
        self.group = group # shiftplan name
        # self.days = db.fetch_days())

        if self.group == "crew":
            shiftplan_pk = db.fetch_shiftplan_pk(name="Crew")
            self.jts = db.fetch_jobtypes(shiftplan_pk)
            self.jobs = db.fetch_jobs(*list(self.jts["id"]))
            self.users = db.fetch_users(shiftplan_pk)
            # self.names = db.fetch_names(helper=False)
            self.preferences = db.fetch_preferences_by_group(self.users, self.jobs)
            # self.exclusives = db.fetch_exclusives()

        elif self.group == "helper":
            self.jts = db.fetch_jobtypes(group="helper")
            self.jobs = db.fetch_jobs_by_group(True)
            self.users = db.fetch_helpers()
            self.names = db.fetch_names(helper=True)
            self.preferences = db.fetch_preferences_by_group("helper")
            self.exclusives = db.fetch_exclusives()
        # print(self.jts)
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
        # print(unregistered_names)
        for id, sn, fn in unregistered_names[["surname", "famname"]].itertuples(index=True):
            self.users = self.users.append(
                {'fullname_id': id, 'nickname': sn+fn, 'break': 4, 'bias': 0, 'workload': 4}, ignore_index=True)
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
        # print(self.preferences.index)
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
