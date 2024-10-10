class Link:

    def __init__(self):
        # only one possible according to documentation
        self.predecessor = None
        self.successor = None


class Predecessor:

    def __init__(self, element_id=None, element_type=None, contact_point=None, element_dir=None):
        self.element_id = element_id
        self.element_type = element_type
        self.contact_point = contact_point
        self.element_dir = element_dir
        self.element_s = None



class Successor(Predecessor):
    """Inherits from predecessor"""
