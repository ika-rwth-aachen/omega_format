class Lanes:

    def __init__(self):
        self.lane_offset = []
        self.lane_section = []


class LaneOffset:

    def __init__(self, s=None, a=None, b=None, c=None, d=None):
        self.s = s
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class LaneSection:

    def __init__(self):
        self.s = None
        self.single_side = None
        self.left_lanes = []
        self.center_lanes = []
        self.right_lanes = []


class Lane:

    def __init__(self):
        self.id = None
        self.type = None
        self.level = None
        self.link = LaneLink()
        self.material = []
        self.speed = []
        self.access =[]
        self.road_mark = []
        self.rule = []
        self.width = []
        self.height =[]
        self.borders = []


class LaneWidth:

    def __init__(self, s_offset=None, a=None, b=None, c=None, d=None):
        self.s_offset = s_offset
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class LaneBorder:

    def __init__(self, s_offset=None, a=None, b=None, c=None, d=None):
        self.s_offset = s_offset
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class LaneLink:

    def __init__(self):
        # here multiple are allowed
        self.predecessor = []
        self.successor = []


class LaneRoadMark:

    def __init__(self, s_offset=None, type=None, weight=None, color=None, material=None, lane_change=None):
        self.s_offset = s_offset
        self.type = type
        self.color = color
        self.material = material
        self.lane_change = lane_change
        self.weight = weight
        self.height = None
        self.width = None


class LaneSpeed:

    def __init__(self, s_offset, max, unit):
        self.s_offset = s_offset
        self.max = max
        self.unit = unit


class LaneMaterial:

    def __init__(self, s_offset=None, surface=None, friction=None, roughness=None):
        self.s_offset = s_offset
        self.surface = surface
        self.friction = friction
        self.roughness = roughness


class LaneAccess:

    def __init__(self, s_offset=None, rule=None, restriction=None):
        self.s_offset = s_offset
        self.rule = rule
        self.restriction = restriction


class LaneRule:

    def __init__(self, s_offset=None, value=None):
        self.s_offset = s_offset
        self.value = value


class LaneHeight:

    def __init__(self, s_offset=None, inner=None, outer=None):
        self.s_offset = s_offset
        self.inner = inner
        self.outer = outer
