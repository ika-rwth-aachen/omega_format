class Reference:

    def __init__(self):
        self.element_type = None
        self.element_id = None
        self.type = None


class SignalReference:

    def __init__(self, s=None, t=None, id=None, orientation=None):
        self.s = s
        self.t = t
        self.id = id
        self.orientation = orientation
        self.validity = []

