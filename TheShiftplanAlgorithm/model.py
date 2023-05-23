from pyscipopt import *
import numpy as np
import pandas as pd
import itertools as it
import logging
import pickle
logging.getLogger('matplotlib.font_manager').disabled = True


class Model:
    def __init__(self, jobs, persons, preferences, groupname=""):
        self.jobs = jobs
        self.persons = persons
        self.preferences = preferences
        self.jobs = self.jobs.reset_index(drop=True)
        self.persons = self.persons.reset_index(drop=True)
        self.preferences = self.preferences.reset_index(drop=True)
        self.groupname = groupname

        self.five = -10
        self.three = 0
        self.one = 6
        self.four = -6  # (self.five + self.three) / 2
        self.two = 3  # (self.three + self.one) / 2

        self.slack_coef_diversity = .5
        self.jobs_until_forced_break = 2

        self.workload_per_person = None

        self.model = scip.Model()
        self.vars = np.empty((len(self.persons.index), len(self.jobs.index)), dtype=object)
        self.num_persons, self.num_jobs = self.vars.shape

        self.durings = self.jobs["during"].to_numpy()
        self.total_workhours = np.sum(self.durings)

        self.slack_objective = 0

    def translate_weights(self):
        self.weights[self.weights == 1] = self.one
        self.weights[self.weights == 2] = self.two
        self.weights[self.weights == 3] = self.three
        self.weights[self.weights == 4] = self.four
        self.weights[self.weights == 5] = self.five
        self.center_weights()

    def center_weights(self):
        # print(self.weights)
        means = self.weights.mean(axis=1)
        means = means.reshape(means.size, 1)
        self.weights = self.weights - means
        # print(self.weights)

    def feed_boolean_constraint(self):
        """Solution matrix should contain boolean values"""
        for i in range(self.num_persons):
            for j in range(self.num_jobs):
                # fuer jede Person und Schicht eine boolean variable.
                self.vars[i, j] = self.model.addVar("p{}j{}".format(i, j), vtype='B')
                self.model.addCons(self.vars[i, j] >= 0)
                self.model.addCons(self.vars[i, j] <= 1)


    def assign_every_job(self):
        """Sum of assigned jobs has to equal number of jobs."""
        # Summe der belegten Schichten muss gleich der Anzahl der Schichten sein.
        self.model.addCons(quicksum([quicksum(i) for i in self.vars]) >= self.num_jobs)


    def assign_every_job_once(self):
        """Adds hard constraint:
        Assign every job only once (every job gets assigned to exactly one person).
        """
        for i in range(self.num_jobs):
            self.model.addCons(quicksum(self.vars.T[i]) <= 1)


    def get_workload_per_person(self):
        raise NotImplementedError()


    def feed_workload_hard_constraint(self):
        """Adds hard constraint:
        Constraint working hours to
        less than or equal the intended workload per person plus self.eps and
        more than or equal the intended workload per person minus self.eps.
        """
        for i in range(self.num_persons):
            upper = self.workload_per_person[i] + self.eps
            lower = self.workload_per_person[i] - self.eps
            self.model.addCons(quicksum(self.vars[i]*self.durings) <= upper)
            self.model.addCons(quicksum(self.vars[i]*self.durings) >= lower)


    def feed_forced_break(self):
        """TODO: Enforces break after self.jobs_until_forced_break shifts as hard constraint.
        """
        pass
        # self.neighbors_per_job = {}
        # for id, end in self.dh.jobs[["abs_end"]].itertuples(index=True):
        #     # print(self.dh.jobs.loc[end == self.dh.jobs['abs_start']])
        #     neighbors = self.dh.jobs.loc[end == self.dh.jobs['abs_start']]
        #     self.neighbors_per_job[id] = list(neighbors.index)
        # n_series_ids = []
        # for id in self.neighbors_per_job:
        #     s = self.get_n_series(3, id)
        #     if s:
        #         n_series_ids.append(tuple(s))
        # # print(set(n_series_ids))
        # for p in range(self.num_persons):
        #     n_series_ids = set(n_series_ids)
        #     for ser in n_series_ids:
        #         self.model.addCons(quicksum(self.vars[p][i]
        #                                     for i in ser) <= self.jobs_until_forced_break)


    def no_fives(self):
        print(self.preferences.loc[self.preferences["rating"] == 5])
        fives = self.preferences.loc[self.preferences["rating"] == 5]
        for user_pk, job_pk in fives[["user", "job"]].itertuples(index=False):
            print(self.persons.loc[self.persons["user_pk"] == user_pk].index)
            user_idx = list(self.persons.loc[self.persons["user_pk"] == user_pk].index)[0]
            job_idx = list(self.jobs.loc[self.jobs["pk"] == job_pk].index)[0]
            self.model.addCons(self.vars[user_idx][job_idx] == 0)


    def feed_conflicts_per_person(self):
        """TODO: break"""
        # print(self.persons)
        for p_id, br in self.persons[["break"]].itertuples(index=True):
            print(50*"_")
            # print(p_id, br)
            conf = self.find_conflicts(br)
            for key in conf:
                # print(conf[key].index)
                # print(50*"_")
                self.model.addCons(quicksum(self.vars[p_id][i] for i in conf[key].index) <= 1)


    def get_n_series(self, depth, id, nb_lst_idx=0, series=[]):
        """Calculates all depth-series of jobs.
        @param depth: length of series
        @param id: start id to look for successor.
        @param nb_lst_idx: neighbor list index
        @param series: current series found."""
        if series == []:
            series.append(id)
        if depth == len(series):
            return series
        else:
            if id not in self.neighbors_per_job:
                return False
            else:
                # print(nb_lst_idx, series)
                # print( self.neighbors_per_job[id][nb_lst_idx])

                nb_lst_idx += 1
                if len(self.neighbors_per_job[id]) <= nb_lst_idx:
                    return False
                series.append(self.neighbors_per_job[id][nb_lst_idx])
                if depth == len(series):
                    return series
                return self.get_n_series(depth, self.neighbors_per_job[id][nb_lst_idx], nb_lst_idx, series)


    def find_conflicts(self, br):
        """Finds conflicting jobs for each job.
        Returns dictionary {job_id: <DataFrame of conflicting jobs>}.
        @param br: individual minimum break between two shifts."""
        conflicts = {}
        # print(self.dh.jobs)
        for id, s, e in self.dh.jobs[["datetime_start", "datetime_end"]].itertuples(index=True):
            # print(id)
            tmp = self.dh.jobs.loc[((self.dh.jobs["datetime_start"] >= s-br) & (self.dh.jobs["datetime_start"] < e+br))
                                   | ((self.dh.jobs["datetime_end"] >= s-br) & (self.dh.jobs["datetime_end"] <= e+br))]
            conflicts[id] = tmp
        return conflicts


    def feed_diversity(self):
        # TODO
        jt_categories = self.dh.jts.groupby("name")
        unique_names = {name: i for i, name in enumerate(self.dh.jts.name.unique())}
        vals = [unique_names[n] for n in self.dh.jts.name]
        self.dh.jts["category"] = vals
        # print(self.dh.jts)
        # jobmap = np.empty(self.vars.size)
        vars_slack = []
        vals = [self.jts.loc[j]["category"] for j in self.dh.jobs["jt_primary"]]
        self.dh.jobs["category"] = vals
        # print(self.dh.jts)
        # categories = list(dJob_categories_ind.values())
        # print(pd.merge(self.dh.jobs, self.dh.jts, on=["jt_primary", id]))
        # print(self.dh.jobs.loc[self.dh.jobs["jt_primary"] == self.dh.jts.index])
        for p in range(self.num_persons):
            for id, cat in self.dh.jobs[["category"]].itertuples(index=True):
                vars_slack.append(self.model.addVar("slack_p{}cat{}".format(p, cat), vtype='I'))
                self.model.addCons(quicksum((self.vars[p][i] for i in range(
                    self.num_jobs) if self.dh.jobs.loc[i]["category"] == cat))-vars_slack[-1] <= 1)
                self.model.addCons(vars_slack[-1] >= 0)
                self.slack_objective = - self.slack_coef_diversity * \
                    vars_slack[-1] + self.slack_objective

    def feed_no_break_softly(self):
        no_break_users = self.dh.users.loc[self.dh.users["break"] == 0].index
        vars_slack = []
        for i in no_break_users:
            vars_slack.append(self.model.addVar("slack_p{}cat{}".format(p, cat), vtype='I'))


    def feed_objective(self):
        # print(self.dh.preferences)
        self.weights = np.empty((self.num_persons, self.num_jobs))
        for i, user_pk in self.persons[["user_pk"]].itertuples(index=True):
            # print(self.dh.preferences.loc[name_id])
            # print(name_id)
            # print(10*"*")
            self.weights[i] = self.preferences.loc[self.preferences["user"] == user_pk]["rating"].to_numpy()
        print(self.weights)
        self.translate_weights()
        self.model.setObjective(
            quicksum(map(quicksum, (self.weights*self.vars)))+self.slack_objective, "maximize")
    #    model.setObjective(quicksum(map(quicksum, (lWeights_flat*vars))), "maximize")
    #    model.setObjective(quicksum(map(quicksum, (lPrios_centered*vars))), "maximize")

    def prt_wl(self):
        """Prints workload per person in german language. """
        print("Insgesamt sind {wh} Stunden zu arbeiten für alle {gn}.".format(
            wh=self.total_workhours, gn=self.groupname))
       

    def optimize(self):
        self.model.writeProblem()
        self.model.optimize()
        try:
            self.solution = np.vectorize(lambda x: self.model.getVal(x))(self.vars)
            self.dh.solution = self.solution
            print(self.solution)
            # np.save('solution', self.solution)
            sols = self.model.getSols()
            self.dh.sols = sols
            # with open("data_handler.pkl", 'wb') as f:
            #     pickle.dump(self.dh, f)
            for i, s in enumerate(sols):
                aval = np.vectorize(lambda x: self.model.getSolVal(s, x))(self.vars)
                with open("{}_sol/solutions{}.pkl".format(self.dh.group, i), 'wb') as f:
                    pickle.dump(aval, f)
        except:
            pass