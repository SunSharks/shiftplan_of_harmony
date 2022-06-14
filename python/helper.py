from mensch import Mensch

class Helper(Mensch):
    """Helper class for all users that don't take part in the normal job distribution algorithm."""
    def __init__(self, name_id, name, min_break, prios=None, workload=None):
        super().__init__(name_id, name, min_break, prios)
        self.workload = workload

    def set_workload(workload):
        self.workload = workload
