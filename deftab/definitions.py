class Definitions:
    def __init__(self):
        self.num_days = self.input_int(
            "Nun gib bitte eine Anzahl an Tagen ein.\n", "Als Eingabe werden nur Ganzzahlen akzeptiert.")
        print(f"Wie heißen diese {self.num_days} Tage?")
        self.days = self.input_list(True, self.num_days)
        print("Bitte gib nun die Schichtbezeichnung(en) an.")
        self.jobnames = self.input_list(def_len=False)

    def __repr__(self):
        return f"---\n{self.num_days} Tage:\n{self.days}\nSchichten:\n{self.jobnames}"

    def input_int(self, cmd, err):
        found = False
        while not found:
            try:
                val = int(input(cmd))
                found = True
                return val
            except ValueError:
                print(err)

    def input_list(self, def_len=False, length=1):
        """length: desired length of list, default is 1."""
        found = False
        while not found:
            val = input("Bitte gib eine kommagetrennte (,) Liste ein.\n").split(",")
            if def_len:
                if len(val) == length:
                    found = True
                    return val
                else:
                    print(f"Eingabe muss genau {length-1} Kommata beinhalten.")
            else:
                print(f"Deine Eingabe: {val}")
                return val


Def = Definitions()
print(Def)
