from pyscipopt import quicksum

import fetch_json_data as db
from model import Model



class NonPrioritizedModel(Model):
    def __init__(self, **kwargs):
        self.slack_coef_jobassign = 5
        super().__init__(**kwargs)
        self.workloads = self.persons["workload"].to_numpy()
        self.build_model()

        self.optimize()

    def build_model(self):
        self.feed_boolean_constraint()
        self.assign_every_job_once()
        self.feed_workload_hard_constraint()
        self.feed_forced_break()
        self.no_fives()
        self.feed_conflicts_per_person()
        self.feed_diversity()
        self.assign_every_job_softly()
        self.feed_objective()

    def feed_workload_hard_constraint(self):
        for i in range(self.num_persons):
            self.model.addCons(quicksum(self.vars[i]*self.durings) <= self.workloads[i])


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
    shiftplan = db.fetch_shiftplan()
    # print(shiftplan["mode_name"])
    jts = db.fetch_jobtypes()
    jobs = db.fetch_jobs(*list(jts["pk"]))
    users = db.fetch_users()
    # subcrews = db.fetch_names(helper=False)
    preferences = db.fetch_preferences(users, jobs)
    model = NonPrioritizedModel(jobs=jobs, persons=users, preferences=preferences, jobtypes=jts, shiftplan=shiftplan)
    
