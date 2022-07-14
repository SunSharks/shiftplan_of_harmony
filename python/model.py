from pyscipopt import *
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
import logging
logging.getLogger('matplotlib.font_manager').disabled = True


class Model:
    def __init__(self, jobs, persons, groupname=""):
        self.groupname = groupname

        self.five = -10
        self.three = 0
        self.one = 5
        self.four = (self.five + self.three) / 2
        self.two = (self.three + self.one) / 2

        self.slack_coef_diversity = 1
        self.slack_coef_fairness = 2
        self.eps = 3     # Toleranzstundenanzahl.
        self.jobs_until_forced_break = 2

        self.jobs = jobs
        self.persons = persons

        self.workload_per_person = None

        self.model = scip.Model()
        self.vars = np.empty((len(self.persons.index), len(self.jobs.index)), dtype=object)
        self.num_persons, self.num_jobs = self.vars.shape
        # print(self.num_persons, self.num_jobs)
        #
        # print(len(self.dh.user_preferences.values), self.num_persons)
        # print(42 in self.dh.user_preferences.values)
        self.durings = self.jobs["during"].to_numpy()
        self.total_workhours = np.sum(self.durings)
        # print("Insgesamt sind {wh} Stunden zu arbeiten für alle {gn}.".format(wh=self.total_workhours, gn=self.groupname))
        # self.break_after_two_shifts()

    def translate_weights(self):
        self.weights[self.weights == 1] = self.one
        self.weights[self.weights == 2] = self.two
        self.weights[self.weights == 3] = self.three
        self.weights[self.weights == 4] = self.four
        self.weights[self.weights == 5] = self.five
        self.center_weights()

    def center_weights(self):
        print(self.weights)
        means = self.weights.mean(axis=1)
        means = means.reshape(means.size, 1)
        self.weights = self.weights - means
        print(self.weights)

    def build_model(self):
        self.feed_boolean_constraint()
        self.assign_every_job()
        self.assign_every_job_once()
        self.get_workload_per_person()
        self.feed_workload_hard_constraint()
        self.feed_forced_break()
        self.feed_conflicts_per_person()
        self.feed_fairness()
        self.feed_diversity()
        self.feed_objective()

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
            self.model.addCons(quicksum(self.vars.T[i]) == 1)

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

    def feed_forced_break(self):
        """Enforces break after self.jobs_until_forced_break shifts as hard constraint.
        """
        self.neighbors_per_job = {}
        for id, end in self.jobs[["abs_end"]].itertuples(index=True):
            # print(self.jobs.loc[end == self.jobs['abs_start']])
            neighbors = self.jobs.loc[end == self.jobs['abs_start']]
            self.neighbors_per_job[id] = list(neighbors.index)
        n_series_ids = []
        for id in self.neighbors_per_job:
            s = self.get_n_series(3, id)
            if s:
                n_series_ids.append(tuple(s))
        # print(set(n_series_ids))
        for p in range(self.num_persons):
            n_series_ids = set(n_series_ids)
            for ser in n_series_ids:
                self.model.addCons(quicksum(self.vars[p][i]
                                            for i in ser) <= self.jobs_until_forced_break)

        # print(self.jobs.loc[self.jobs["abs_end"] == self.jobs["abs_start"]])

        # Keiner muss 3 Schichten direkt hintereinander machen.
        # for p in range(self.num_persons):
        #     for j in range(self.num_jobs):
        #         for i in range(j+1, self.num_jobs):
        #             if (translate_linear_time(lJobs[j].begin)[0] == 0 and (translate_linear_time(lJobs[i].begin)[0] == 6 or translate_linear_time(lJobs[i].begin)[0] == 8) and (translate_linear_time(lJobs[j].begin)[1] == translate_linear_time(lJobs[i].begin)[1])) or ((translate_linear_time(lJobs[j].end)[0] == 0 and translate_linear_time(lJobs[i].begin)[0] == 4) and translate_linear_time(lJobs[j].end)[1] == translate_linear_time(lJobs[i].begin)[1]) :
        #                 model.addCons(vars[p][j] + vars[p][i] <= 1)

        # print(10*'='+"\nNow entering long permutations loop.\n"+10*'=')
        # for p in range(_p):
        #     for j1, j2, j3 in it.permutations(self.jobs, 3):
        #     #    print(j1.name, j2.name, j3.name)
        #         if j1.end == j2.begin and j2.end == j3.begin:
        #             model.addCons(vars[p][j1.id]*lJobs[j1.id].during + vars[p][j2.id]*lJobs[j2.id].during + vars[p][j3.id]*lJobs[j3.id].during <= 10)
        # print('finally.')

    def find_conflicts(self, br):
        """Finds conflicting jobs for each job.
        Returns dictionary {job_id: <DataFrame of conflicting jobs>}.
        @param br: individual minimum break between two shifts."""
        conflicts = {}
        # print(self.jobs)
        for id, s, e in self.jobs[["abs_start", "abs_end"]].itertuples(index=True):
            # print(id)
            tmp = self.jobs.loc[((self.jobs["abs_start"] >= s-br) & (self.jobs["abs_start"] < e+br))
                                | ((self.jobs["abs_end"] >= s-br) & (self.jobs["abs_end"] <= e+br))]
            conflicts[id] = tmp
            # conflicts.update(id=tmp)
            # print(self.jobs.loc[((self.jobs["abs_start"] >= s) & (self.jobs["abs_start"] < e)) | ((self.jobs["abs_end"] >= s) & (self.jobs["abs_end"] <= e))]["id"])
        # print(conflicts)
        # conflicts = pd.DataFrame(conflicts.items(), columns=["jobid", "conflicting_job_ids"])
        # print(conflicts.tail())
        # conflicts.set_index("jobid")
        # assert 1==0
        return conflicts

    def feed_conflicts_per_person(self):
        for p_id, br in self.persons[["break"]].itertuples(index=True):
            # print(50*"_")
            conf = self.find_conflicts(br)
            print(br)
            for key in conf:
                self.model.addCons(quicksum(self.vars[p_id][i] for i in conf[key].index) <= 1)

    def feed_fairness(self):
        """ TODO!
        Adds vars to model:
        - slack_upper_fairness
        - slack lower fairness

        """

        self.vars_slack_fairness = []
        self.slack_objective = 0

        for p in range(self.num_persons):
            self.vars_slack_fairness.append(self.model.addVar(
                "slack_upper_fairness_p{}".format(p), vtype='I'))
            self.model.addCons(
                quicksum(self.vars[p]*self.durings)-self.vars_slack_fairness[-1] <= self.workload_per_person[p])
            self.model.addCons(self.vars_slack_fairness[-1] >= 0)
            self.slack_objective = -self.slack_coef_fairness * \
                self.vars_slack_fairness[-1] + self.slack_objective

            self.vars_slack_fairness.append(self.model.addVar(
                "slack_lower_fairness_p{}".format(p), vtype='I'))
            self.model.addCons(quicksum(self.vars[p] * self.durings) +
                               self.vars_slack_fairness[-1] >= self.workload_per_person[p])
            self.model.addCons(self.vars_slack_fairness[-1] >= 0)
            self.slack_objective = - self.slack_coef_fairness * \
                self.vars_slack_fairness[-1] + self.slack_objective

    def feed_diversity(self):
        # TODO
        jt_categories = self.dh.jts.groupby("name")
        print()
        unique_names = {name: i for i, name in enumerate(self.dh.jts.name.unique())}
        vals = [unique_names[n] for n in self.dh.jts.name]
        self.dh.jts["category"] = vals
        # print(self.dh.jts)
        # jobmap = np.empty(self.vars.size)
        vars_slack = []
        vals = [self.dh.jts.loc[j]["category"] for j in self.jobs["jt_primary"]]
        self.jobs["category"] = vals
        # print(self.dh.jts)
        # categories = list(dJob_categories_ind.values())
        # print(pd.merge(self.dh.jobs, self.dh.jts, on=["jt_primary", id]))
        # print(self.dh.jobs.loc[self.dh.jobs["jt_primary"] == self.dh.jts.index])
        for p in range(self.num_persons):
            for id, cat in self.jobs[["category"]].itertuples(index=True):
                vars_slack.append(self.model.addVar("slack_p{}cat{}".format(p, cat), vtype='I'))
                self.model.addCons(quicksum((self.vars[p][i] for i in range(
                    self.num_jobs) if self.jobs.loc[i]["category"] == cat))-vars_slack[-1] <= 1)
                self.model.addCons(vars_slack[-1] >= 0)
                self.slack_objective = - self.slack_coef_diversity * \
                    vars_slack[-1] + self.slack_objective

    def feed_objective(self):
        # print(self.dh.preferences)
        self.weights = np.empty((self.num_persons, self.num_jobs))
        for id, name_id in self.persons[["fullname_id"]].itertuples(index=True):
            self.weights[id] = self.dh.preferences.loc[name_id].to_numpy()
        # print(weights)
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
        self.solution = np.vectorize(lambda x: self.model.getVal(x))(self.vars)
        np.save('solution', self.solution)

    def panda_solution(self):
        sol_df = pd.DataFrame(self.solution)
        print(self.jobs)
        print(self.num_jobs)
        # sol_df.columns = [self.dh.jts.loc[self.jobs.loc[i]["jt_primary"]]["name"]
        #                   for i in range(self.num_jobs)]
        sol_df.columns = self.jobs.index
        sol_df.index = [self.persons.loc[p]["nickname"] for p in range(self.num_persons)]
        print(self.dh.days)
        for d in self.dh.days:
            for p_id, p in self.persons[["nickname"]].itertuples(index=True):
                plt.plot(np.arange(self.num_jobs), self.solution[p_id, :], 'o', label=p)
                plt.legend()
                plt.show()
