

class Day:
    def __init__(self, id, name, date):
        self.id = id
        self.name = name
        self.date = date

    def __repr__(self):
        s = """Day: {id}
        name: {name} date: {date}""".format(id=self.id, name=self.name, date=self.date)
        return s
