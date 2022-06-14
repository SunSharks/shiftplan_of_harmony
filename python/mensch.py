
menschen = {}
class Mensch:
    global counter
    def __init__(self, name_id, name, min_break, prios=None):
        self.name_id = name_id
        self.name = name
        self.min_break = min_break
        self.prios = prios
        self.prios_flat = flatten(prios)
        self.APPROVED = False
        self.bias = 0
        self.conflicts = None
        self.jobs_assigned = None
        global menschen
        menschen[self.name_id] = self
    #    string_comps = [map_of_competences[i] for i in self.competences]
    #    print(string_comps)
#        print("init erfolgreich. name: " + self.name + " Kompetenzen: " + map_of_competences[])
        #self.nacht = nacht
        #assert type(nacht)==bool
        # NACHTREGELUNG, jeder muss mind. 1x in nacht arbeiten+++++++++++++++++++++TODO
        # flexible Schichten
        # gemeinsame Schichten

    def set_prios(prios):
        self.prios = prios
