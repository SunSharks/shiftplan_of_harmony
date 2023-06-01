import numpy as np
# import matplotlib.pyplot as plt
import itertools
import json
import os
from datetime import datetime
import pickle

class Solution:
    def __init__(self, model, solutions_path="../TheShiftplan/sols/_json/_admin/{}.json"):
        self.solutions = model.solutions
        self.jobs = model.jobs
        self.persons = model.persons
        self.preferences = model.preferences
        self.jobtypes = model.jobtypes
        self.shiftplan = model.shiftplan
        self.solutions_path = solutions_path
        self.complete_solutions_path()

        self.preferences_np = self.preferences.to_numpy()
        # self.style = ""
        # # self.run_plt()
        # self.get_most_popular_jobs()
        # self.get_last_popular_jobs()
        # self.get_avg_rate()
        # self.get_avg_rate_per_job()
        self.solution_lists = {}
        for i, s in enumerate(self.solutions):
            self.solution_lists[i] = self.create_user_job_assigned(s)
        self.write_json(json.dumps(self.solution_lists))


    def create_user_job_assigned(self, solution):
        """
        Returns user_job_assigned list of dicts for a single solution.
        [
            {
                "user": <user_pk>,
                "job": <job_pk>,
                "assigned": <True/False>
            }, ...
        ]
        @param solution: numpy.ndarray
        """
        user_job_assigned = []
        for j in self.jobs.index:
            job = int(self.jobs.iloc[j]["pk"])
            assigned_persons = np.where(solution[:,j] == 1)
            unassigned_persons = np.where(solution[:,j] != 1)
            assigned_users = list(self.persons.iloc[assigned_persons]["user_pk"])
            unassigned_users = list(self.persons.iloc[unassigned_persons]["user_pk"])
            instances = [
                {
                    "user": user,
                    "job": job,
                    "assigned": True
                } for user in assigned_users
            ]
            instances.extend([
                {
                    "user": user,
                    "job": job,
                    "assigned": False
                } for user in unassigned_users
            ])
            user_job_assigned.extend(instances)
        return user_job_assigned


    def complete_solutions_path(self):
        now = datetime.now()
        date_str = datetime.strftime(now, '%Y-%m-%d-%H-%M')
        file_timestamp = f"{date_str}"
        self.solutions_path = self.solutions_path.format(file_timestamp)
        
            
    def write_json(self, json_str):
        with open(self.solutions_path, 'w') as f:
            f.write(json_str)


    def get_color_palette(self):
        palette = sns.color_palette("coolwarm", np.unique(self.avg_rates).shape[0]).as_hex()[::-1]
        unique_vals = {val: i for i, val in enumerate(np.unique(self.avg_rates))}
        for j, av in zip(self.jobs.index, self.avg_rates):
            self.style += "#job{j} !border: 5px solid {c};?".format(j=j, c=palette[unique_vals[av]])

    def get_color_map(self):
        html = "<div id=colormap></div>"

    def get_most_popular_jobs(self):
        self.avg_most_pop = np.min(self.preferences_np.sum(axis=0))/self.preferences_np.shape[0]
        self.most_pop_idx = np.where(self.preferences_np.sum(axis=0) ==
                                     np.min(self.preferences_np.sum(axis=0)))[0]

    def get_last_popular_jobs(self):
        self.avg_last_pop = np.max(self.preferences_np.sum(axis=0))/self.preferences_np.shape[0]
        self.last_pop_idx = np.where(self.preferences_np.sum(axis=0) ==
                                     np.max(self.preferences_np.sum(axis=0)))[0]
        # print(self.last_pop_idx)

    def get_avg_rate(self):
        self.avg_rate = self.preferences_np.sum() / self.preferences_np.size

    def get_avg_rate_per_job(self):
        self.avg_rates = self.preferences_np.sum(axis=0)/self.preferences_np.shape[0]

    def run_plt(self):
        self.build_ticklabels()
        for i, row in enumerate(self.dh.solution):
            personal_solution = self.solution_row_to_jobmask(row)
            self.draw_one_person(personal_solution, i)

        # im1 = plt.imshow(self.jobmask, cmap=plt.cm.gray)
        # plt.show()

    def solution_row_to_jobmask(self, row):
        personal_solution = self.jobmask
        # print(self.sol_idx_to_mask_idx[i])
        # print(self.jobmask[self.sol_idx_to_mask_idx[i][0],
        #                    self.sol_idx_to_mask_idx[i][1]:self.sol_idx_to_mask_idx[i][2]])
        assigned_jobs = self.dh.jobs.loc[np.where(row >= .9)]
        for aj in assigned_jobs.index:
            tup = self.sol_idx_to_mask_idx[aj]
            personal_solution[tup[0], tup[1]:tup[2]] += 1
        return personal_solution

    def build_ticklabels(self):
        self.ylabels = self.dh.jts["name"].tolist()
        self.xlabels = [i % 24 for i in range(len(self.dh.days.index)*24)]

    def draw_one_person(self, personal_solution, i):
        fig, ax = plt.subplots(1, 1)
        im = plt.imshow(personal_solution, aspect='auto', cmap=plt.cm.gray, alpha=.5)
        im = plt.imshow(self.id_jobmask, aspect='auto', cmap='hot', alpha=.1)

        # plt.xlabel('x label')
        # plt.ylabel('y label')
        ax.set_xticks(np.arange(0, len(self.dh.days.index)*24))
        ax.set_yticks(np.arange(len(self.dh.jts.index)))
        ax.set_xticklabels(self.xlabels)
        ax.set_yticklabels(self.ylabels)
        plt.title("Schichtplan für {}".format(self.dh.users.loc[i]["nickname"]))
        curr_job = -1
        for i, j in itertools.product(range(personal_solution.shape[0]), range(personal_solution.shape[1])):
            if personal_solution[i, j] == 2:
                if curr_job != self.id_jobmask[i, j]:
                    # tup = self.sol_idx_to_mask_idx[]
                    # middle = tup[2] - tup[1] // 2
                    text = "{}-{}\nUhr".format(
                        self.dh.jobs.loc[self.id_jobmask[i, j]]["dt_start"], self.dh.jobs.loc[self.id_jobmask[i, j]]["dt_end"])
                    plt.text(j+self.dh.jobs.loc[self.id_jobmask[i, j]]["during"]//2,
                             i, text, ha="center", va="center", color="green")
                    curr_job = self.id_jobmask[i, j]

        # fig.colorbar(im)
        plt.show()

    def get_assigned_job_str(self, name, job_id):
        print("*** {jobname} Beginn: {beg_day} {beg_time} Uhr Ende: {end_day} {end_} Uhr, Nacht: {}. Gewählt mit Note: {}".format(lJobs[j[0]].name, translate_linear_time(lJobs[j[0]].begin)[
              1], translate_linear_time(lJobs[j[0]].begin)[0], translate_linear_time(lJobs[j[0]].end)[1], translate_linear_time(lJobs[j[0]].end)[0], lJobs[j[0]].nacht, lPersons[p].prios_flat[j[0]]))

    def show_solution(self):
        self.solution = np.vectorize(lambda x: self.model.getVal(x))(self.vars)
        # data = [df1["A"], df2["A"]]
        # headers = ["df1", "df2"]
        # df3 = pd.concat(data, axis=1, keys=headers)
        print(self.solution)
        print((self.solution >= 0.9).nonzero())

        # print(self.dh.jts["name"])
        # print(self.dh.jts.loc[self.jobs["jt_primary"]])

        for row in self.solution:
            pers_nonzeros = (row >= 0.9).nonzero()[0]
            print(pers_nonzeros)
            sol = {}
            for id, dayname, date in self.dh.days[["name", "date"]].itertuples(index=True):

                # print((row >= 0.9).nonzero()[0])
                pers_jobs = self.jobs.iloc[(row >= 0.9).nonzero()[0]]

        def show_solution(self):
            string = ""
            cnt = 0
            for p in range(self.num_persons):
                selfjobs = []
                # print(self.dh.preferences)
                print("{} ist in folgende Schichten eingeteilt worden: ".format(
                    self.persons.loc[p]["nickname"]))
                string += "{} ist in folgende Schichten eingeteilt worden: ".format(
                    self.persons.loc[p]["nickname"])
                print(10*'-=- ')
                string += 10*'-=- '
                print('Pausenoption: {}'.format(self.persons.loc[p]["break"]))
                string += 'Pausenoption: {}'.format(self.persons.loc[p]["break"])
                for j in enumerate(self.solution[p]):
                    # print(j[1])
                    if j[1] > 0:
                        if j[1] >= 0.9:
                            cnt += 1
                            print("*** {} Beginn: {} {} Uhr Ende: {} {} Uhr. Gewählt mit Note: {}".format(
                                self.dh.jts.loc[self.jobs.loc[j[0]]["jt_primary"]]["name"], self.jobs.loc[j[0]]["start_day_id"], self.jobs.loc[j[0]]["dt_start"], self.jobs.loc[j[0]]["end_day_id"], self.jobs.loc[j[0]]["dt_end"], self.dh.preferences.loc[self.persons.loc[p]["fullname_id"]]["job{}".format(self.jobs.loc[j[0]]["id"])]))
                            string += "*** {} Beginn: {} {} Uhr Ende: {} {} Uhr. Gewählt mit Note: {}".format(
                                self.dh.jts.loc[self.jobs.loc[j[0]]["jt_primary"]]["name"], self.jobs.loc[j[0]]["start_day_id"], self.jobs.loc[j[0]]["dt_start"], self.jobs.loc[j[0]]["end_day_id"], self.jobs.loc[j[0]]["dt_end"], "TODO")
                        else:
                            print(100*'_')
                            print("***NICHT: {} Beginn: {} {} Uhr Ende: {} {} Uhr. Gewählt mit Note: {}".format(
                                self.dh.jts.loc[self.jobs.loc[j[0]]["jt_primary"]]["name"], self.jobs.loc[j[0]]["start_day_id"], self.jobs.loc[j[0]]["dt_start"], self.jobs.loc[j[0]]["end_day_id"], self.jobs.loc[j[0]]["dt_end"], "TODO"))
                            print(100*"_")
                # print(lPersons[p].prios)
                # print(10*'-+- ')
                # print(sum(np.array([j.during for j in selfjobs])) + lPersons[p].bias)
                '''
                print(lPersons[p].prios_flat)
                '''
            # print(sum([sum(i) for i in aVal]))
            # print(cnt)
            return string
