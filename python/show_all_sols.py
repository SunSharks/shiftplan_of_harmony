import pickle
from solution import Solution
import sys

folder = sys.argv[1]


class Data_Handler:
    def __init__(self, days, jts, jobs, users, names, preferences, exclusives, solution, group):
        self.days = days
        self.jts = jts
        self.jobs = jobs
        self.users = users
        self.names = names
        self.preferences = preferences
        self.exclusives = exclusives
        self.solution = solution
        self.group = group


filenames = ["days.pkl", "jts.pkl", "jobs.pkl", "users.pkl",
             "names.pkl", "preferences.pkl", "exclusives.pkl"]
dhs = []
solutions = []
for fi in filenames:
    with open(folder + fi, 'rb') as f:
        dhs.append(pickle.load(f))

for i in range(int(sys.argv[2])):
    with open(folder + "solutions{}.pkl".format(i), 'rb') as f:
        solutions.append(pickle.load(f))


for i, s in enumerate(solutions):
    dh = Data_Handler(*dhs, s, group="helper")
    s = Solution(dh, id=i)
