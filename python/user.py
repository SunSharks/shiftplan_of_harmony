from mensch import Mensch

class User(Mensch):
    """User class for all 'normal' users. (Not helpers)"""
    def __init__(self, name_id, name, min_break, prios=None, bias=None):
        super().__init__(name_id, name, min_break, prios)
        self.bias = bias

    def set_bias(bias):
        self.bias = bias
