
from pyscipopt import *
import numpy as np
import pandas as pd
import itertools as it

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
        self.vars = np.empty((len(self.persons.index),len(self.jobs.index)), dtype=object)
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

    def build_model(self):
        self.feed_boolean_constraint()
        self.assign_every_job()
        self.assign_every_job_once()
        self.get_workload_per_person()
        self.feed_workload_hard_constraint()
        self.feed_forced_break()
        self.feed_conflicts_per_person()
        self.feed_fairness()

        self.feed_objective()

    def feed_boolean_constraint(self):
        """Solution matrix should contain boolean values"""
        for i in range(self.num_persons):
            for j in range(self.num_jobs):
                self.vars[i,j] = self.model.addVar("p{}j{}".format(i,j), vtype='B') # fuer jede Person und Schicht eine boolean variable.
                self.model.addCons(self.vars[i,j] >= 0)
                self.model.addCons(self.vars[i,j] <= 1)

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
                self.model.addCons(quicksum(self.vars[p][i] for i in ser) <= self.jobs_until_forced_break)


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


    def feed_conflicts_per_person(self):
        for p_id, br in self.persons[["break"]].itertuples(index=True):
            # print(50*"_")
            conf = self.find_conflicts(br)
            # print(conf)
            for key in conf:
                self.model.addCons(quicksum(self.vars[p_id][i] for i in conf[key].index) <= 1)
        # === Konflikte === TODO
        # lConflicts = conflicting_pausenoption(self.persons, self.jobs)
        # for p in self.persons:
        #     for i in p.conflicts:
        #         for j in p.conflicts[i]:
        #             model.addCons(vars[p.id, i.id] + vars[p.id, j.id] <= 1)

    def feed_fairness(self):
        """ TODO!
        Adds vars to model:
        - slack_upper_fairness
        - slack lower fairness

        """

        self.vars_slack_fairness = []
        self.slack_objective = 0

        for p in range(self.num_persons):
            self.vars_slack_fairness.append(self.model.addVar("slack_upper_fairness_p{}".format(p), vtype='I'))
            self.model.addCons(quicksum(self.vars[p]*self.durings)-self.vars_slack_fairness[-1] <= self.workload_per_person[p])
            self.model.addCons(self.vars_slack_fairness[-1] >= 0)
            self.slack_objective = -self.slack_coef_fairness*self.vars_slack_fairness[-1] + self.slack_objective

            self.vars_slack_fairness.append(self.model.addVar("slack_lower_fairness_p{}".format(p), vtype='I'))
            self.model.addCons(quicksum(self.vars[p] * self.durings) + self.vars_slack_fairness[-1] >= self.workload_per_person[p])
            self.model.addCons(self.vars_slack_fairness[-1] >= 0)
            self.slack_objective = - self.slack_coef_fairness * self.vars_slack_fairness[-1] + self.slack_objective



    def feed_objective(self):
        print(self.dh.preferences)
        self.weights = np.empty((self.num_persons, self.num_jobs))
        for id, name_id in self.persons[["fullname_id"]].itertuples(index=True):
            self.weights[id] = self.dh.preferences.loc[name_id].to_numpy()
        # print(weights)
        self.translate_weights()
        self.model.setObjective(quicksum(map(quicksum, (self.weights*self.vars)))+self.slack_objective, "maximize")
    #    model.setObjective(quicksum(map(quicksum, (lWeights_flat*vars))), "maximize")
    #    model.setObjective(quicksum(map(quicksum, (lPrios_centered*vars))), "maximize")




    def prt_wl(self):
        """Prints workload per person in german language. """
        print("Insgesamt sind {wh} Stunden zu arbeiten für alle {gn}.".format(wh=self.total_workhours, gn=self.groupname))

    def get_assigned_job_str(name, job_id):
        print("*** {jobname} Beginn: {beg_day} {beg_time} Uhr Ende: {end_day} {end_} Uhr, Nacht: {}. Gewählt mit Note: {}".format(lJobs[j[0]].name, translate_linear_time(lJobs[j[0]].begin)[1], translate_linear_time(lJobs[j[0]].begin)[0], translate_linear_time(lJobs[j[0]].end)[1], translate_linear_time(lJobs[j[0]].end)[0], lJobs[j[0]].nacht, lPersons[p].prios_flat[j[0]]))

    def show_solution(self):
        self.solution = np.vectorize(lambda x: self.model.getVal(x))(self.vars)
        np.save('solution', self.solution)
        # data = [df1["A"], df2["A"]]
        # headers = ["df1", "df2"]
        # df3 = pd.concat(data, axis=1, keys=headers)

        print(self.solution >= 0.9)
        # print(self.dh.jts["name"])
        # print(self.dh.jts.loc[self.jobs["jt_primary"]])

        for row in self.solution:
            sol = {}
            for id, dayname, date in self.dh.days[["name", "date"]].itertuples(index=True):

            # print((row >= 0.9).nonzero()[0])
                pers_jobs = self.jobs.iloc[(row >= 0.9).nonzero()[0]]



        # string = ""
        # print(self.persons)
        # for p, name, br in self.persons[["fullname_id", "break"]].itertuples(index=True):
        #     selfjobs = []
        #     print("{} ist in folgende Schichten eingeteilt worden: ".format(name))
        #     string += "{} ist in folgende Schichten eingeteilt worden: ".format(name)
        #     print(10*'-=- ')
        #     string += 10*'-=- '
        #     print('Pausenoption: {}'.format(br))
        #     string += 'Pausenoption: {}'.format(br)
        #     for i, j in enumerate(self.solution[p]):
        #         #print(j[1])
        #         if j > 0:
        #             if j >= 0.9:
        #                 print("Assigned to job: \n {}".format(self.jobs.iloc[[i]]))
        #
        #     print(10*'-+- ')

        print(sum([sum(i) for i in self.solution]))
        # return string

    def optimize(self):
        self.model.writeProblem()
        self.model.optimize()
        self.solution = np.vectorize(lambda x: self.model.getVal(x))(self.vars)
