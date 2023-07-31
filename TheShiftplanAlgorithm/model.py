from pyscipopt import *
import numpy as np
import pandas as pd
import itertools as it
import logging
import pickle
import os
from datetime import timedelta


logging.getLogger('matplotlib.font_manager').disabled = True


class Model:
    def __init__(self, jobs=None, persons=None, preferences=None, jobtypes=None, shiftplan=None, subcrews=None):
        self.jobs = jobs
        self.persons = persons
        self.preferences = preferences
        self.jobtypes = jobtypes
        self.shiftplan = shiftplan
        self.subcrews = subcrews

        self.jobs = self.jobs.reset_index(drop=True)
        self.persons = self.persons.reset_index(drop=True)
        self.preferences = self.preferences.reset_index(drop=True)
        self.biases = self.persons["bias"].to_numpy()
        # logging.debug(self.biases)
        # logging.info(len(self.jobs.index))

        self.five = -10
        self.three = 0
        self.one = 6
        self.four = -6  # (self.five + self.three) / 2
        self.two = 3  # (self.three + self.one) / 2

        self.slack_coef_diversity = .5
        self.max_time_frame = timedelta(hours=10)
        self.jobs_until_forced_break = 2

        self.workload_per_person = None

        self.model = scip.Model()
        self.vars = np.empty((len(self.persons.index), len(self.jobs.index)), dtype=object)
        self.num_persons, self.num_jobs = self.vars.shape

        self.durings = self.jobs["during"].to_numpy()
        self.total_workhours = np.sum(self.durings)
        self.priorities = self.jobs["priority"].to_numpy()

        self.slack_objective = 0

        self.build_weights()


    def build_weights(self):
        self.weights = np.empty((self.num_persons, self.num_jobs))
        # logging.debug(self.persons)
        for i, user_pk, un in self.persons[["user_pk", "nickname"]].itertuples(index=True):
            self.weights[i] = self.preferences.loc[self.preferences["user"] == user_pk]["rating"].to_numpy()
            # logging.debug(un)
            # logging.debug(self.preferences.loc[self.preferences["user"] == user_pk]["rating"].to_numpy())
            
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
        # logging.debug(self.persons)
        # self.model.addCons(quicksum([quicksum(i) for i in self.vars]) >= self.num_jobs)
        for i in range(self.num_jobs):
            self.model.addCons(quicksum(self.vars.T[i]) >= 1)


    def assign_every_job_once(self):
        """Adds hard constraint:
        Assign every job only once (every job gets assigned to exactly one person).
        """
        for i in range(self.num_jobs):
            self.model.addCons(quicksum(self.vars.T[i]) <= 1)


    def assign_every_job_softly(self):
        self.vars_slack_jobassign = []
        for j in range(self.num_jobs):
            self.vars_slack_jobassign.append(self.model.addVar("slack_j{}".format(j), vtype='I'))
            self.model.addCons(quicksum(self.vars[p][j] for p in range(
                self.num_persons))+self.vars_slack_jobassign[-1] >= 1)
            self.model.addCons(self.vars_slack_jobassign[-1] >= 0)
            self.slack_objective = - self.slack_coef_jobassign * \
                self.vars_slack_jobassign[-1] + self.slack_objective


    def prioritize_jobs(self):
        # print(len(self.jobs.index))
        # print(len(self.persons.index))
        # print(self.weights.shape)
        self.weights = self.weights + self.priorities * self.prioritized_weights_coef


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


    def consider_subcrews(self):
        for id, sc_pk, members, sc_name in self.subcrews[["pk", "members", "name"]].itertuples(index=True):
            jts = list(self.jobtypes.loc[self.jobtypes["subcrew"] == sc_pk]["pk"])
            if len(jts) == 0:
                continue
            # logging.debug(sc_name)
            # logging.debug(jts)
            jobs = self.jobs[self.jobs['jobtype'].isin(jts)]
            # logging.debug(jobs)
            excluded_persons = self.persons[~self.persons['pk'].isin(members)]
            # logging.debug(excluded_persons)
            excluded_persons_pd_idx = list(excluded_persons.index)
            jobs_pd_idx = list(jobs.index)
            subcrew_prefs = self.preferences[self.preferences['user'].isin(members)]
            # logging.debug(subcrew_prefs)
            for j_pk in list(jobs["pk"]):
                prefs = subcrew_prefs.loc[subcrew_prefs["job"] == j_pk]["rating"]
                # logging.debug(set(prefs))
                set_prefs = set(prefs)
                if set_prefs == {5}:
                    logging.warning("Restricted Job only rated by 5.")
            if len(excluded_persons_pd_idx) + len(jobs_pd_idx) >= 2:
                for p in excluded_persons_pd_idx:
                    logging.debug(self.preferences.at[p, 'rating'])
                    self.preferences.at[p, 'rating'] = 5
                    # logging.debug(self.preferences.at[p, 'rating'])
                    # self.model.addCons(quicksum(self.vars[p][j] for j in jobs_pd_idx) <= 0)
                    # for j in jobs_pd_idx:
                    #     logging.debug(self.vars)
                    #     self.model.addCons(self.vars[p][j] <= 0)
            



    def get_job_successors(self):
        self.job_successors = {}
        for id, end, during in self.jobs[["datetime_end", "during"]].itertuples(index=True):
            successors = self.jobs.loc[end == self.jobs['datetime_start']]
            self.job_successors[id] = list(successors.index)


    def feed_conflicting_series(self, ser):
        l = len(ser) - 1
        for p in range(self.num_persons):
            self.model.addCons(quicksum(self.vars[p][i] for i in ser) <= l)


    def feed_forced_break(self):
        """TODO: Enforces break after self.max_time_frame hours as hard constraint.
        """
        self.get_job_successors()
        
        for id, during in self.jobs[["during"]].itertuples(index=True):
            during = timedelta(hours=during)
            if during >= self.max_time_frame:
                for nb_id in self.job_successors[id]:
                    self.feed_conflicting_series([id, nb_id])
                    # logging.debug(self.jobs.iloc[nb_id]["during"])
            else:
                max_n = 5
                n = 3
                while n < max_n:
                    s = self.get_n_series(n, id)
                    # logging.debug(s)
                    if s:
                        durs = self.jobs.iloc[s]["during"].sum()
                        # logging.debug(self.jobs.iloc[s]["datetime_end"])
                        if timedelta(hours=durs) >= self.max_time_frame:
                            self.feed_conflicting_series(s)
                            break
                    else:
                        break     
                    n += 1
        


    def no_fives(self):
        fives = self.preferences.loc[self.preferences["rating"] == 5]
        # Check feasibility
        only_fives_found = False
        # logging.debug(self.jobs)
        for job_pk, jt_pk, begin, end in self.jobs[["pk", "jobtype", "datetime_start", "datetime_end"]].itertuples(index=False):
            jobs = self.preferences.loc[self.preferences["job"] == job_pk]
            # logging.debug(jobs.loc[jobs["rating"] != 5])
            if len(jobs.loc[jobs["rating"] != 5].index) == 0:
                jobtype = self.jobtypes.loc[self.jobtypes["pk"] == jt_pk].at[0, "name"]
                logging.warning(f"Every user rated this job with 5:\n{jobtype} {begin} - {end}")
                only_fives_found = True
        if only_fives_found:
            logging.warning("Continuing with a model that will not be able to fully avoid assignments that are rated 5.")
            return 
        
        logging.info("There are no jobs exclusively rated by 5.")
        for user_pk, job_pk in fives[["user", "job"]].itertuples(index=False):
            user_idx = list(self.persons.loc[self.persons["user_pk"] == user_pk].index)[0]
            job_idx = list(self.jobs.loc[self.jobs["pk"] == job_pk].index)[0]
            self.model.addCons(self.vars[user_idx][job_idx] == 0)


    def feed_conflicts_per_person(self):
        """TODO: break"""
        # print(self.persons)
        for p_id, br in self.persons[["break"]].itertuples(index=True):
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
            if id not in self.job_successors:
                return False
            else:
                # print(nb_lst_idx, series)
                # print( self.job_successors[id][nb_lst_idx])

                nb_lst_idx += 1
                if len(self.job_successors[id]) <= nb_lst_idx:
                    return False
                series.append(self.job_successors[id][nb_lst_idx])
                if depth == len(series):
                    return series
                return self.get_n_series(depth, self.job_successors[id][nb_lst_idx], nb_lst_idx, series)


    def find_conflicts(self, br):
        """Finds conflicting jobs for each job.
        Returns dictionary {job_id: <DataFrame of conflicting jobs>}.
        @param br: individual minimum break between two shifts."""
        conflicts = {}
        # print(self.jobs)
        for id, s, e in self.jobs[["datetime_start", "datetime_end"]].itertuples(index=True):
            tmp = self.jobs#.drop(id)
            tmp = tmp.loc[(tmp["datetime_start"] >= s-br) & (tmp["datetime_start"] < e+br)]
            # print(tmp)

            conflicts[id] = tmp
        return conflicts


    def feed_diversity(self):
        """
        Feed jobtype diversity soft constraint.
        """
        vars_slack = []
        vals = [list(self.jobtypes.loc[self.jobtypes["pk"] == j]["name"])[0] for j in self.jobs["jobtype"]]
        self.jobs["category"] = vals
        for p in range(self.num_persons):
            for id, cat in self.jobs[["category"]].itertuples(index=True):
                vars_slack.append(self.model.addVar("slack_p{}cat{}".format(p, cat), vtype='I'))
                self.model.addCons(quicksum((self.vars[p][i] for i in range(
                    self.num_jobs) if self.jobs.loc[i]["category"] == cat))-vars_slack[-1] <= 1)
                self.model.addCons(vars_slack[-1] >= 0)
                self.slack_objective = - self.slack_coef_diversity * \
                    vars_slack[-1] + self.slack_objective


    def feed_no_break_softly(self):
        no_break_users = self.persons.loc[self.persons["break"] == 0].index
        vars_slack = []
        for i in no_break_users:
            vars_slack.append(self.model.addVar("slack_p{}cat{}".format(p, cat), vtype='I'))


    def feed_objective(self):
        self.model.setObjective(
            quicksum(map(quicksum, (self.weights*self.vars)))+self.slack_objective, "maximize")
    #    model.setObjective(quicksum(map(quicksum, (lWeights_flat*vars))), "maximize")
    #    model.setObjective(quicksum(map(quicksum, (lPrios_centered*vars))), "maximize")


    def prt_wl(self):
        """Prints workload per person in german language. """
        print("Insgesamt sind {wh} Stunden zu arbeiten für alle {gn}.".format(
            wh=self.total_workhours, gn=self.shiftplan_name))
       

    def optimize(self):
        self.model.writeProblem()
        self.model.optimize()
        solutions = self.model.getSols()
        self.solutions = []
        for i, s in enumerate(solutions):
            aval = np.vectorize(lambda x: self.model.getSolVal(s, x))(self.vars)
            self.solutions.append(aval)
        logging.info(self.solutions)
        # for num, l in enumerate(self.solutions[0]):
        #     for num2, i in enumerate(l):
        #         if i == 1:
        #             pass
                    # print(50*'*')
                    # print(self.persons.iloc[num], "\nassigned\n", self.jobs.iloc[num2])
                    # print(50*'-')


    def dump_solutions_pkl(self):
        mode_name = self.shiftplan["mode_name"]
        shiftplan_name = self.shiftplan["shiftplan_name"]
        solution_path = os.path.join("solution_pkls", f"{mode_name}", f"{shiftplan_name}")
        if not os.path.exists(solution_path):
            os.makedirs(solution_path)
        curr_try = len(os.listdir(solution_path))
        run_path = os.path.join(solution_path, f"run{curr_try}")
        os.mkdir(run_path)
        for i, s in enumerate(self.solutions):
            out_path = os.path.join(run_path, f"solution{i}.pkl")
            with open(out_path, 'wb') as f:
                pickle.dump(s, f)

