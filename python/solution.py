import numpy as np
import matplotlib.pyplot as plt
import itertools


class Solution:
    def __init__(self, dh):
        self.dh = dh
        self.get_jobmask()
        self.run()

    def get_jobmask(self):
        """Returns a (<number of jobypes> x <number of days>*24) sized numpy array
        with entries equal 1 if there is a shift at this time and 0 if not.
        """
        self.jobmask = np.zeros((len(self.dh.jts.index), len(self.dh.days.index)*24))
        self.id_jobmask = np.ones((len(self.dh.jts.index), len(self.dh.days.index)*24))*-1
        self.sol_idx_to_mask_idx = {}
        for i, (id, name) in enumerate(self.dh.jts[["name"]].itertuples(index=True)):
            jt_jobs = self.dh.jobs.loc[self.dh.jobs["jt_primary"] == id]
            for index, abs_start, abs_end in jt_jobs[["abs_start", "abs_end"]].itertuples(index=True):
                self.jobmask[i, abs_start:abs_end] = 1
                self.id_jobmask[i, abs_start:abs_end] = index
                self.sol_idx_to_mask_idx[index] = (i, abs_start, abs_end)
        print(self.jobmask)

    def run(self):
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
        assigned_jobs = self.dh.jobs.loc[np.where(row == 1)]
        for aj in assigned_jobs.index:
            tup = self.sol_idx_to_mask_idx[aj]
            personal_solution[tup[0], tup[1]:tup[2]] += 1
        return personal_solution

    def build_ticklabels(self):
        self.ylabels = self.dh.jts["name"].tolist()
        self.xlabels = [i % 24 for i in range(len(self.dh.days.index)*24)]

    def draw_one_person(self, personal_solution, i):
        fig, ax = plt.subplots(1, 1)
        im = plt.imshow(personal_solution, aspect='auto', cmap=plt.cm.gray)

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
                    text = "{} \n-\n{}\n Uhr".format(
                        self.dh.jobs.loc[self.id_jobmask[i, j]]["dt_start"], self.dh.jobs.loc[self.id_jobmask[i, j]]["dt_end"])
                    plt.text(j, i, text, ha="center", va="center", color="green")
                    curr_job = self.id_jobmask[i, j]

        # fig.colorbar(im)
        plt.show()

    def panda_solution(self):
        print(self.dh.days)
        print(self.dh.jobs)
        print(self.dh.jts)
        print(self.persons)
        self.visualizer = Visualizer(self.solution)
        self.get_jobmask()
        self.solution_row_to_jobmask()

        colors = ("grey", "green", "red")
        for index, nickname, br, bias in self.persons[["nickname", "break", "bias"]].itertuples(index=True):
            pers_line = self.solution[index, :]
            # line_per_jt =
            for id, name, date in self.dh.days[["name", "date"]].itertuples(index=True):
                print(id, name, date)

        # print(self.dh.jobs)
        # print(self.num_jobs)
        self.img_sol = self.solution * 255
        # sol_df.columns = [self.dh.jts.loc[self.dh.jobs.loc[i]["jt_primary"]]["name"]
        #                   for i in range(self.num_jobs)]
        # sol_df.columns = self.dh.jobs.index
        # sol_df.index = [self.persons.loc[p]["nickname"] for p in range(self.num_persons)]

        # image = Image.fromarray(self.img_sol)
        # image.show()

        # print(self.dh.days)
        # for d in self.dh.days:
        #     for p_id, p in self.persons[["nickname"]].itertuples(index=True):
        # plt.plot(np.arange(self.num_jobs), self.solution[p_id, :], 'o', label=p)
        # plt.legend()
        # plt.show()

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

    def panda_solution(self):
        sol_df = pd.DataFrame(self.solution)
        sol_df.columns = []

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
