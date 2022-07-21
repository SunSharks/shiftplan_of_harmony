import data_handler
from solution import Solution
import pandas as pd
from model import Model

from pyscipopt import quicksum
import numpy as np
import logging


class User_Model(Model):
    def __init__(self):
        self.slack_coef_fairness = 2
        self.eps = 8     # Toleranzstundenanzahl.

        self.dh = data_handler.Data_Handler()
        self.dh.users = self.dh.users[self.dh.users["nickname"].str.contains("funkloch") == False]
        # print(self.dh.users)
        super().__init__(self.dh.jobs, self.dh.users, groupname="Mitglieder der Crew")
        self.biases = self.persons["bias"].to_numpy()

        self.build_model()

        # self.prt_avg_workload_per_person()
        # self.prt_biased_workloads()

        self.optimize()

    def build_model(self):
        self.feed_boolean_constraint()
        self.assign_every_job()
        self.assign_every_job_once()
        self.get_workload_per_person()
        self.feed_workload_hard_constraint()
        self.feed_forced_break()
        self.feed_conflicts_per_person()
        self.feed_night_constraint()
        self.feed_fairness()
        self.feed_diversity()
        self.feed_objective()

    def assign_every_job(self):
        """Sum of assigned jobs has to equal number of jobs."""
        # Summe der belegten Schichten muss gleich der Anzahl der Schichten sein.
        self.model.addCons(quicksum([quicksum(i) for i in self.vars]) >= self.num_jobs)

    def get_workload_per_person(self):
        # self.biases = self.df.jobs[during].to_numpy()
        self.workload_per_person = (np.ones(
            self.num_persons) * ((self.total_workhours + sum(self.biases)) / self.num_persons)) - self.biases
        # print(self.workload_per_person)

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

    def feed_night_constraint(self):
        nightjobs = self.dh.jobs.loc[(self.dh.jobs["dt_start"] >= 0) &
                                     (self.dh.jobs["dt_start"] <= 8)].index
        for p in range(self.num_persons):
            if len(nightjobs) < self.num_persons:
                self.model.addCons(quicksum(self.vars[p][i] for i in nightjobs) <= 1)
            else:
                self.model.addCons(quicksum(self.vars[p][i] for i in nightjobs) >= 1)

        # self.model.addCons(quicksum())
        print("Folgende Schichten finden in der Nacht statt:\n{}\n".format(nightjobs))
        return

    def feed_fairness(self):
        """ TODO!
        Adds vars to model:
        - slack_upper_fairness
        - slack lower fairness

        """

        self.vars_slack_fairness = []

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

    def prt_avg_workload_per_person(self):
        logging.info("Das wären im Optimalfall {avg} Stunden für jeden ohne Beachtung von Ausnahmen.".format(
            avg=self.total_workhours/self.num_persons))

    def prt_biased_workloads(self):
        i = 0
        # print(self.persons)
        for name, bias in self.persons[["nickname", "bias"]].itertuples(index=False):
            logging.info("{n} muss {b} Stunden weniger Arbeiten als die anderen und arbeitet so im Optimalfall {wolo} Stunden.".format(
                n=name, b=bias, wolo=self.workload_per_person[i]))
            i += 1
        return


if __name__ == "__main__":
    model = User_Model()
    s = Solution(model.dh)
