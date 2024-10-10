class ObjectOutlines:

    def __init__(self):
        self.objectOutlines = []


class ObjectOutline:

    def __init__(self):
        self.id = None
        self.fill_type = None
        self.outer = None
        self.closed = None
        self.lane_type = None
        self.outline_geometry = None


class OutlineGeometry:

    def __init__(self):
        self.corner_road = []
        self.corner_local = []


class OutlineCornerRoad:

    def __init__(self, s = None, t = None, dz = None, height = None, id = None):
        self.s = s
        self.t = t
        self.dz = dz
        self.height = height
        self.id = id


class OutlineCornerLocal:

    def __init__(self, u = None, v = None, z = None, height = None, id = None):
        self.u = u
        self.v = v
        self.z = z
        self.height = height
        self.id = id
