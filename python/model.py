import data_handler

from pyscipopt import *
import numpy as np
import itertools as it

class Model:
    def __init__(self):
        self.five = -10
        self.three = 0
        self.one = 5
        self.four = (self.five + self.three) /2
        self.two = (self.three + self.one) /2

        self.slack_coef_diversity =1
        self.slack_coef_fairness = 2
        self.eps = 3     # Toleranzstundenanzahl.
        self.dh = data_handler.Data_Handler()

        self.model = scip.Model()
        self.vars = np.empty((len(self.dh.users.index),len(self.dh.crew_jobs.index)), dtype=object)
        self.num_persons, self.num_jobs = self.vars.shape
        # print(self.num_persons, self.num_jobs)
        #
        # print(len(self.dh.user_preferences.values), self.num_persons)
        # print(42 in self.dh.user_preferences.values)
        self.total_workhours = self.dh.crew_jobs["during"].sum()
        print(self.total_workhours)
        self.build_model()
        self.assign_every_job()
        self.assign_every_job_once()
        self.get_workload_per_person()



    def build_model(self):
        for i in range(self.num_persons):
            for j in range(self.num_jobs):
                self.vars[i,j] = self.model.addVar("p{}j{}".format(i,j), vtype='B') # fuer jede Person und Schicht eine boolean variable.
                self.model.addCons(self.vars[i,j]>=0)
                self.model.addCons(self.vars[i,j]<=1)

    def assign_every_job(self):
        # Summe der belegten Schichten muss gleich der Anzahl der Schichten sein.
        self.model.addCons(quicksum([quicksum(i) for i in self.vars]) >= self.num_jobs)

    def assign_every_job_once(self):
        # Jede Schicht soll nur durch eine Person belegt sein.
        for i in range(self.num_jobs):
            self.model.addCons(quicksum(self.vars.T[i]) == 1)

    def get_workload_per_person(self):
        # biases = self.df.crew_jobs[during].to_numpy()
        biases = self.dh.users["bias"].to_numpy()
        print(biases)

        # lSumBiases = sum(lBiases) * np.ones(_p)
        # lStunden_gesamt = stunden_gesamt * np.ones(self.num_persons)
        # lLenP = _p * np.ones(_p)
        # Sollstunden_je_pers =  (np.ones(_p) * ((stunden_gesamt + sum(lBiases)) / _p)) - lBiases
        # stunden_gesamt += sum(lBiases)
        # avghours = stunden_gesamt/_p
        # print("Bei {} Stunden Gesamtarbeitszeit und {} Personen muss jeder in etwa {:.4f} Stunden arbeiten.".format(stunden_gesamt, _p, avghours))
        # sollstunden = np.array([avghours-p.bias for p in lPersons]) # bei AlexB aufpassen/anpassen->(bias = 20)
        # assert _j*_p == vars.shape[0]*vars.shape[1]
        # lDurings = np.array(lDurings)
        # for i in range(_p):
        #     model.addCons(quicksum(vars[i]*lDurings) <= Sollstunden_je_pers[i]+EPS)
        #     model.addCons(quicksum(vars[i]*lDurings) >= Sollstunden_je_pers[i]-EPS)


    def fairness(self):
        # ===FAIRNESS===

        vars_slack_fairness = []
        slack_objective = 0

        for p in range(_p):
            vars_slack_fairness.append(model.addVar("slack_upper_fairness_p{}".format(p), vtype='I'))
            model.addCons(quicksum(vars[p]*lDurings)-vars_slack_fairness[-1] <= Sollstunden_je_pers[p])
            model.addCons(vars_slack_fairness[-1] >= 0)
            slack_objective = -slack_coef_fairness*vars_slack_fairness[-1] + slack_objective

            vars_slack_fairness.append(model.addVar("slack_lower_fairness_p{}".format(p), vtype='I'))
            model.addCons(quicksum(vars[p] * lDurings) + vars_slack_fairness[-1] >= Sollstunden_je_pers[p])
            model.addCons(vars_slack_fairness[-1] >= 0)
            slack_objective = -slack_coef_fairness * vars_slack_fairness[-1] + slack_objective





    def build_model_old(lJobs, lPersons, lWeights):
        '''
        input:  lJobs: list of jobs instances.
                lPersons: list of mensch instances.
                lWeights[Pers,Job,Slot]: list of weights per timeslot per jobtype per person.
                                        ("translated", but not flattened)
                delt: Bestrafungsgewicht fuer Softconstraints. ---> TODO
            '''

        _w = len(lWeights)
        _p = len(lPersons)
        _j = len(lJobs)

        lDurings = [j.during for j in lJobs]
        lWeights_flat = np.empty((_p,_j))     # Matrix of shape (#Pers, #Jobs)
        assert _w == _p
        for i in range(_p):
            # Hol dir Indices der Leute mit Ausnahmen.
            if lPersons[i].name == 'Sascha Quadt':
                IDsascha = lPersons[i].id
            elif lPersons[i].name == 'Alexander Bonas':
                IDAlex = lPersons[i].id
            elif lPersons[i].name == 'Jonas Thormeier':
                IDJONES = lPersons[i].id
            #    print(lPersons[i].name, lPersons[i].id)
            lWeights_flat[i] = flatten(lWeights[i]) * np.array(lDurings)     # that stores weight per job.
        #print(len(lWeights_flat), len(lWeights_flat[0]))
        model = scip.Model()
        vars = np.empty((_p,_j), dtype=object)
        for i in range(_p):
            for j in range(_j):
                vars[i,j] = model.addVar("p{}j{}".format(i,j), vtype='B') # fuer jede Person und Schicht eine boolean variable.
                model.addCons(vars[i,j]>=0)
                model.addCons(vars[i,j]<=1)





        lPrios_centered = center_prios(lWeights_flat)
    #    print(lPrios_centered)

        # Keiner muss 3 Schichten direkt hintereinander machen.
        for p in range(_p):
            for j in range(_j):
                for i in range(j+1, _j):
                    if (translate_linear_time(lJobs[j].begin)[0] == 0 and (translate_linear_time(lJobs[i].begin)[0] == 6 or translate_linear_time(lJobs[i].begin)[0] == 8) and (translate_linear_time(lJobs[j].begin)[1] == translate_linear_time(lJobs[i].begin)[1])) or ((translate_linear_time(lJobs[j].end)[0] == 0 and translate_linear_time(lJobs[i].begin)[0] == 4) and translate_linear_time(lJobs[j].end)[1] == translate_linear_time(lJobs[i].begin)[1]) :
                        if p != IDAlex:
                            model.addCons(vars[p][j] + vars[p][i] <= 1)

        # Summe der belegten Schichten muss gleich der Anzahl der Schichten sein.
        model.addCons(quicksum([quicksum(i) for i in vars]) >= len(lJobs))

        # Jede Schicht soll nur durch eine Person belegt sein.
        for i in range(_j):
            model.addCons(quicksum(vars.T[i]) == 1)



        # ===FAIRNESS===
        EPS = 3     # Toleranzstundenanzahl.
        lBiases = np.array([j.bias for j in lPersons])
        stunden_gesamt = sum([j.during for j in lJobs])
        lSumBiases = sum(lBiases) * np.ones(_p)
        lStunden_gesamt = stunden_gesamt * np.ones(_p)
        lLenP = _p * np.ones(_p)
        Sollstunden_je_pers =  (np.ones(_p) * ((stunden_gesamt + sum(lBiases)) / _p)) - lBiases
        stunden_gesamt += sum(lBiases)
        avghours = stunden_gesamt/_p
        print("Bei {} Stunden Gesamtarbeitszeit und {} Personen muss jeder in etwa {:.4f} Stunden arbeiten.".format(stunden_gesamt, _p, avghours))
        sollstunden = np.array([avghours-p.bias for p in lPersons]) # bei AlexB aufpassen/anpassen->(bias = 20)
        assert _j*_p == vars.shape[0]*vars.shape[1]
        lDurings = np.array(lDurings)
        for i in range(_p):
            model.addCons(quicksum(vars[i]*lDurings) <= Sollstunden_je_pers[i]+EPS)
            model.addCons(quicksum(vars[i]*lDurings) >= Sollstunden_je_pers[i]-EPS)

        vars_slack_fairness = []
        slack_objective = 0

        for p in range(_p):
            vars_slack_fairness.append(model.addVar("slack_upper_fairness_p{}".format(p), vtype='I'))
            model.addCons(quicksum(vars[p]*lDurings)-vars_slack_fairness[-1] <= Sollstunden_je_pers[p])
            model.addCons(vars_slack_fairness[-1] >= 0)
            slack_objective = -slack_coef_fairness*vars_slack_fairness[-1] + slack_objective

            vars_slack_fairness.append(model.addVar("slack_lower_fairness_p{}".format(p), vtype='I'))
            model.addCons(quicksum(vars[p] * lDurings) + vars_slack_fairness[-1] >= Sollstunden_je_pers[p])
            model.addCons(vars_slack_fairness[-1] >= 0)
            slack_objective = -slack_coef_fairness * vars_slack_fairness[-1] + slack_objective

        # EXCEPTIONS:
            # Sascha uebernimmt nur Technik-Kunstbuehne-Schichten:
    #    nichtsaschasschichten = [i for i in range(_j) if "technik" not in lJobs[i].name.lower()]
        #print([lJobs[i].name for i in nichtsaschasschichten])
        #print(lJobs)
        #assert 0==1
        """
        for i in nichtsaschasschichten:
            model.addCons(vars[IDsascha][i] == 0)
        # Schichten, die Alex uebernimmt.
        alex_info = ('Betreuung Alternative', 24, 48, 52)
        alex_schichten = [i for i in range(_j) if lJobs[i].name == alex_info[0] and (lJobs[i].begin == alex_info[1] or lJobs[i].begin == alex_info[2])]
        for i in alex_schichten:
            model.addCons(vars[IDAlex][i] == 1)
        #    print(lJobs[i].name, translate_linear_time(lJobs[i].begin))
        #  Jones macht auch nur Alternative
        not_betr_alt = [i for i in range(_j) if lJobs[i].name != "Betreuung Alternative"]
        for i in not_betr_alt:
            model.addCons(vars[IDJONES][i] == 0)

        """
        # === Abwechslung ===
        dJob_categories, dJob_categories_ind = get_job_categories(lJobs)
        jobmap = np.empty(vars.size)
        vars_slack = []
        #slack_objective = 0
        categories = list(dJob_categories_ind.values())


        for p in range(_p):
            for cat in categories:
                vars_slack.append(model.addVar("slack_p{}cat{}".format(p,cat), vtype='I'))
                model.addCons(quicksum((vars[p][i] for i in range(_j) if dJob_categories_ind[i]==cat))-vars_slack[-1]<=1)
                model.addCons(vars_slack[-1]>=0)
                slack_objective = - slack_coef_diversity*vars_slack[-1] + slack_objective


        # === Konflikte ===
        lConflicts = conflicting_pausenoption(lPersons, lJobs)
        for p in lPersons:
            for i in p.conflicts:
                for j in p.conflicts[i]:
                    model.addCons(vars[p.id, i.id] + vars[p.id, j.id] <= 1)


        # === Keine 3 Schichten hintereinander ===
        print(10*'='+"\nNow entering long permutations loop.\n"+10*'=')
        for p in range(_p):
            for j1, j2, j3 in it.permutations(lJobs, 3):
            #    print(j1.name, j2.name, j3.name)
                if j1.end == j2.begin and j2.end == j3.begin:
                    model.addCons(vars[p][j1.id]*lJobs[j1.id].during + vars[p][j2.id]*lJobs[j2.id].during + vars[p][j3.id]*lJobs[j3.id].during <= 10)
        print('finally.')

    # === Nicht 2x dieselbe zeit ===
        for p in range(_p):
            #for j1, j2 in it.permutations():
            pass

        for p in range(_p):
            model.addCons(quicksum(vars[p])<=5)               # jeder macht max. 5 Schichten.
            model.addCons(quicksum(vars[p])>=1)               # jeder macht mind 1 schicht.
            model.addCons(quicksum(vars[p][-5:]) <= 1)        # Verteile die 5 Wasserschichten auf die mind. 5 Leute.
        model.setObjective(quicksum(map(quicksum, (lWeights_flat*vars)))+slack_objective, "maximize")
    #    model.setObjective(quicksum(map(quicksum, (lWeights_flat*vars))), "maximize")
    #    model.setObjective(quicksum(map(quicksum, (lPrios_centered*vars))), "maximize")

        model.writeProblem()
    #    print(_j)
        return model, vars

if __name__ == "__main__":
    model = Model()
