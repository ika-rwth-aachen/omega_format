class Junction:

    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.s_start = None
        self.s_end = None
        self.connection = []
        self.priority = []
        self.controller = []
        self.surface = []


class JunctionConnection:

    def __init__(self):
        self.id = None
        self.incoming_road = None
        self.connecting_road = None
        self.contact_point = None
        self.type = None
        self.lane_link = []
        # only one or zero possible
        self.predecessor = JunctionPredecessor()
        self.successor = JunctionSuccessor()


class JunctionPredecessor:

    def __init__(self):
        self.element_type = None
        self.element_id = None
        self.element_s = None
        self.element_dir = None


class JunctionSuccessor(JunctionPredecessor):
    """Inherits from Predecessor"""


class JunctionLaneLink:
    # from not usable since it is internal parameter
    def __init__(self, from_value=None, to=None):
        self.from_value = from_value
        self.to = to


class JunctionPriority:

    def __init__(self, high=None, low=None):
        self.high = high
        self.low = low


class JunctionController:

    def __init__(self, id=None):
        self.id = id
        self.type = None
        self.sequence = None


class JunctionSurface:

    def __init__(self):
        self.crg = []


class JunctionSurfaceCrg:

    def __init__(self, file=None, mode=None, purpose=None, z_offset=None, z_scale=None):
        self.file = file
        self.mode = mode
        self.purpose = purpose
        self.z_offset = z_offset
        self.z_scale = z_scale
