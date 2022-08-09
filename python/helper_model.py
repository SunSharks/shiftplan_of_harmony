from pyscipopt import quicksum
import data_handler
from model import Model
from solution import Solution


class Helper_Model(Model):
    def __init__(self):
        self.slack_coef_jobassign = 2
        self.dh = data_handler.Data_Handler("helper", "Helfende")
        super().__init__(self.dh.jobs, self.dh.users, groupname="Helfende")
        self.workloads = self.persons["workload"].to_numpy()
        self.build_model()

        # self.prt_avg_workload_per_person()
        # self.prt_biased_workloads()

        self.optimize()

    def build_model(self):
        self.feed_boolean_constraint()
        self.assign_every_job_once()
        self.feed_workload_hard_constraint()
        self.feed_forced_break()
        self.feed_conflicts_per_person()
        self.feed_diversity()
        self.assign_every_job_softly()
        self.feed_objective()

    def feed_workload_hard_constraint(self):
        print(self.workloads)
        for i in range(self.num_persons):
            self.model.addCons(quicksum(self.vars[i]*self.durings) <= self.workloads[i])

    def assign_every_job_softly(self):
        self.vars_slack_jobassign = []
        for j in range(self.num_jobs):
            self.vars_slack_jobassign.append(self.model.addVar("slack_j{}".format(j), vtype='I'))
            self.model.addCons(quicksum(self.vars[p][j] for p in range(
                self.num_persons))+self.vars_slack_jobassign[-1] >= 1)
            self.model.addCons(self.vars_slack_jobassign[-1] >= 0)
            self.slack_objective = - self.slack_coef_jobassign * \
                self.vars_slack_jobassign[-1] + self.slack_objective

    # def priorize_times(self):
    #     self.vars_slack_priotimes = []
    #     for j in range(self.num_jobs):
    #         self.vars_slack_priotimes.append(self.model.addVar("slack_j{}".format(j), vtype='I'))
    #         self.model.addCons(quicksum(self.vars[p][j] for p in range(
    #             self.num_persons))+self.vars_slack_priotimes[-1] >= 1)
    #         self.model.addCons(self.vars_slack_priotimes[-1] >= 0)
    #         self.slack_objective = - self.slack_coef_jobassign * \
    #             self.vars_slack_priotimes[-1] + self.slack_objective


if __name__ == "__main__":
    model = Helper_Model()
    s = Solution(model.dh)
