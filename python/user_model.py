import data_handler
from solution import Solution
import pandas as pd
from model import Model

from pyscipopt import quicksum
import numpy as np
import logging


class User_Model(Model):
    def __init__(self):
        self.dh = data_handler.Data_Handler()
        self.dh.users = self.dh.users[self.dh.users["nickname"].str.contains("funkloch") == False]
        # print(self.dh.users)
        super().__init__(self.dh.jobs, self.dh.users, groupname="Mitglieder der Crew")
        self.biases = self.persons["bias"].to_numpy()
        self.slack_coef_diversity = 1

        self.build_model()
        self.feed_night_constraint()

        self.prt_avg_workload_per_person()
        self.prt_biased_workloads()

        self.optimize()

    def get_workload_per_person(self):
        # self.biases = self.df.jobs[during].to_numpy()
        self.workload_per_person = (np.ones(
            self.num_persons) * ((self.total_workhours + sum(self.biases)) / self.num_persons)) - self.biases
        # print(self.workload_per_person)

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
