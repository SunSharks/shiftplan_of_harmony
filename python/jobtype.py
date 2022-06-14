
crew_jobs = {}
helper_jobs = {}



class Jobtype:
    def __init__(db_id, name, competences, special, helper):
        self.id = db_id
        self.name = name
        self.competences = competences
        self.special = special
        self.helper = helper
        if helper:
            helper_jobs[self.id] = self
        else:
            crew_jobs[self.id] = self

    def __repr__():
        s = """Jobtype: {id} {name}
        special: {special}, helper: {helper} \n\n
        {comps}
        """.format(id=self.id, name=self.name, special=self.special, helper=self.helper, comps=self.competences)
