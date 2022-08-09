import numpy as np
# import matplotlib.pyplot as plt
import itertools
import seaborn as sns


class Solution:
    def __init__(self, dh, id=""):
        self.dh = dh
        self.id = id
        self.preferences_np = self.dh.preferences.to_numpy()
        self.style = ""
        self.get_jobmask()
        # self.run_plt()
        self.get_most_popular_jobs()
        self.get_last_popular_jobs()
        self.get_avg_rate()
        self.get_avg_rate_per_job()

        self.get_color_palette()

        self.get_stats_style()
        self.get_htmls()

    def get_color_palette(self):
        palette = sns.color_palette("coolwarm", np.unique(self.avg_rates).shape[0]).as_hex()[::-1]
        unique_vals = {val: i for i, val in enumerate(np.unique(self.avg_rates))}
        for j, av in zip(self.dh.jobs.index, self.avg_rates):
            self.style += "#job{j} !border: 5px solid {c};?".format(j=j, c=palette[unique_vals[av]])

    def get_color_map(self):
        html = "<div id=colormap></div>"

    def get_most_popular_jobs(self):
        self.avg_most_pop = np.min(self.preferences_np.sum(axis=0))/self.preferences_np.shape[0]
        self.most_pop_idx = np.where(self.preferences_np.sum(axis=0) ==
                                     np.min(self.preferences_np.sum(axis=0)))[0]

    def get_last_popular_jobs(self):
        self.avg_last_pop = np.max(self.preferences_np.sum(axis=0))/self.preferences_np.shape[0]
        self.last_pop_idx = np.where(self.preferences_np.sum(axis=0) ==
                                     np.max(self.preferences_np.sum(axis=0)))[0]
        # print(self.last_pop_idx)

    def get_avg_rate(self):
        self.avg_rate = self.preferences_np.sum() / self.preferences_np.size

    def get_avg_rate_per_job(self):
        self.avg_rates = self.preferences_np.sum(axis=0)/self.preferences_np.shape[0]

    def get_stats_style(self):
        for i in self.most_pop_idx:
            self.style += "#job{mp} !background-color: green;?".format(mp=i)
        for i in self.last_pop_idx:
            self.style += "#job{lp} !background-color: red;?".format(lp=i)
        self.style = self.style.replace("!", "{")
        self.style = self.style.replace("?", "}")
        # print(self.style)

    def get_htmls(self):
        with open("html_skel.html", "r") as f:
            self.html_skel = f.read()
        # time_nickname_html = self.get_html(self.insert_time_nickname)
        # self.time_nickname_html = self.html_skel.format(
        #     STYLE=self.style, MODE=" mit Zeiten", TABLE=time_nickname_html)
        # with open("{}_sol/time_nickname_tab{}.html".format(self.dh.group, self.id), "w") as f:
        #     f.write(self.time_nickname_html)
        # self.html_skel = ""
        nickname_pref_html = self.get_html(self.insert_nickname_pref)
        self.nickname_pref_html = self.html_skel.format(
            STYLE=self.style, MODE=" mit Präferenzen", TABLE=nickname_pref_html)
        with open("{}_sol/nickname_pref_tab{}.html".format(self.dh.group, self.id), "w") as f:
            f.write(self.nickname_pref_html)

        nickname_html = self.get_html(self.insert_nickname)
        self.nickname_html = self.html_skel.format(STYLE=self.style, MODE="", TABLE=nickname_html)
        with open("{}_sol/nickname_tab{}.html".format(self.dh.group, self.id), "w") as f:
            f.write(self.nickname_html)

    def insert_nickname_pref(self, id, **kwargs):
        try:
            assigned_user = np.where(self.dh.solution[:, id] >= .9)[0][0]
            assigned_nickname = self.dh.users.loc[assigned_user]["nickname"]
            name_id = self.dh.users.loc[assigned_user]["fullname_id"]
            pref = self.dh.preferences.loc[name_id].to_numpy()[id]
            inp = "<strong>{}</strong><br>{}".format(assigned_nickname, int(pref))
        except IndexError:
            inp = ""
        return inp

    def insert_nickname(self, id, **kwargs):
        try:
            assigned_user = np.where(self.dh.solution[:, id] >= .9)[0][0]
            assigned_nickname = self.dh.users.loc[assigned_user]["nickname"]
            inp = "<strong>{}</strong>".format(assigned_nickname)
        except IndexError:
            inp = ""
        return inp

    def insert_time_nickname(self, id, **kwargs):
        try:
            assigned_user = np.where(self.dh.solution[:, id] >= .9)[0][0]
            assigned_nickname = self.dh.users.loc[assigned_user]["nickname"]
            inp = "{} - {} Uhr<br><strong>{}</strong>".format(
                kwargs["dt_start"], kwargs["dt_end"], assigned_nickname)
        except IndexError:
            inp = ""
        return inp

    def get_html(self, insert):
        html = """<table id="tab" border="5" cellspacing="0" align="center">
        <!--<caption>{caption}</caption>-->
        <tr> <!-- DAYNAME ROW -->
        <td rowspan="2" align="center" height="50">
            <b>Job/Time</b>
        </td>
        """.format(caption="Schichtplan für ")
        for name, d in self.dh.days[["name", "date"]].itertuples(index=False):
            html += "<td colspan='24' align='center' height='50'><b>{n}</b></td>".format(n=name)
        html += "</tr><tr> <!-- DAYTIME ROW -->"
        for name in self.dh.days[["name"]].itertuples():
            for i in range(24):
                b = ""
                if i < 10:
                    b = "&nbsp;"
                b += str(i)
                html += "<td align='center' height='50'><b>{}</b></td>".format(b)
        html += "</tr>"
        html += "<!-- JOBTYPE ROWS -->"
        odd_style = "style='background-color:#edf9e1'"
        even_style = "style='background-color:#d3e3c4'"
        # odd_style = ""
        # even_style = ""
        for id, name, comp in self.dh.jts[["name", "competences"]].itertuples(index=True):
            style = odd_style
            title = "title='{c}'".format(c=comp)
            html += "<tr {s}>".format(s=style)
            html += "<th {t} class='rowhead' align='left' height='50'><b>{n}</b></th>".format(
                t=title, n=name)
            idx = 0
            for id, dur, abs_start, abs_end in self.dh.jobs.loc[self.dh.jobs["jt_primary"] == id][["during", "abs_start", "abs_end"]].itertuples(index=True):
                inp = insert(id, dur=dur, abs_start=abs_start, abs_end=abs_end)
                while idx < abs_start:
                    if idx % 2 == 0:
                        style = even_style
                    else:
                        style = odd_style
                    html += "<td {s} align='center' width='20px' height='50'></td>".format(s=style)
                    idx += 1
                html += "<div><td id=job{id} {s} colspan='{d}' align='center' height='50'>{inp}</td></div>".format(
                    id=id, s=style, d=dur, inp=inp)
                idx = abs_end
            while idx <= len(self.dh.days.index)*24:
                if idx % 2 == 0:
                    style = even_style
                else:
                    style = odd_style
                html += "<td $style align='center'  height='50'></td>"
                idx += 1
            html += "</tr>"
        html += "</table>"
        return html

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
        # print(self.jobmask)

    def run_plt(self):
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
        assigned_jobs = self.dh.jobs.loc[np.where(row >= .9)]
        for aj in assigned_jobs.index:
            tup = self.sol_idx_to_mask_idx[aj]
            personal_solution[tup[0], tup[1]:tup[2]] += 1
        return personal_solution

    def build_ticklabels(self):
        self.ylabels = self.dh.jts["name"].tolist()
        self.xlabels = [i % 24 for i in range(len(self.dh.days.index)*24)]

    def draw_one_person(self, personal_solution, i):
        fig, ax = plt.subplots(1, 1)
        im = plt.imshow(personal_solution, aspect='auto', cmap=plt.cm.gray, alpha=.5)
        im = plt.imshow(self.id_jobmask, aspect='auto', cmap='hot', alpha=.1)

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
                    # tup = self.sol_idx_to_mask_idx[]
                    # middle = tup[2] - tup[1] // 2
                    text = "{}-{}\nUhr".format(
                        self.dh.jobs.loc[self.id_jobmask[i, j]]["dt_start"], self.dh.jobs.loc[self.id_jobmask[i, j]]["dt_end"])
                    plt.text(j+self.dh.jobs.loc[self.id_jobmask[i, j]]["during"]//2,
                             i, text, ha="center", va="center", color="green")
                    curr_job = self.id_jobmask[i, j]

        # fig.colorbar(im)
        plt.show()

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
