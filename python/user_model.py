import data_handler

from model import Model

import numpy as np
import logging

class User_Model(Model):
    def __init__(self):
        self.dh = data_handler.Data_Handler()
        self.dh.users = self.dh.users[self.dh.users["nickname"].str.contains("funkloch")==False]
        # print(self.dh.users)
        super().__init__(self.dh.jobs, self.dh.users, groupname="Mitglieder der Crew")
        self.biases = self.persons["bias"].to_numpy()

        self.build_model()

        self.prt_avg_workload_per_person()
        self.prt_biased_workloads()


    def get_workload_per_person(self):
        # self.biases = self.df.jobs[during].to_numpy()
        self.workload_per_person = (np.ones(self.num_persons) * ((self.total_workhours + sum(self.biases)) / self.num_persons)) - self.biases
        # print(self.workload_per_person)

    def prt_avg_workload_per_person(self):
        logging.info("Das wären im Optimalfall {avg} Stunden für jeden ohne Beachtung von Ausnahmen.".format(avg=self.total_workhours/self.num_persons))

    def prt_biased_workloads(self):
        i = 0
        # print(self.persons)
        for name, bias in self.persons[["nickname", "bias"]].itertuples(index=False):
            logging.info("{n} muss {b} Stunden weniger Arbeiten als die anderen und arbeitet so im Optimalfall {wolo} Stunden.".format(n=name, b=bias, wolo=self.workload_per_person[i]))
            i += 1

if __name__ == "__main__":
    model = User_Model()
