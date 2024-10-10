class Objects:

    def __init__(self):
        self.tunnel = []
        self.bridge = []
        self.object_reference = []
        self.object = []


class ObjectsTunnel:

    def __init__(self, s=None, length=None, name=None, id=None, type=None, lighting=None, daylight=None):
        self.s = s
        self.length = length
        self.name = name
        self.id = id
        self.type = type
        self.lighting = lighting
        self.daylight = daylight
        self.validity = []


class ObjectsBridge:

    def __init__(self, s=None, length=None, name=None, id=None, type=None):
        self.s = s
        self.length = length
        self.name = name
        self.id = id
        self.type = type
        self.validity = []


class ObjectsReference:

    def __init__(self, s=None, t=None, id=None, orientation=None):
        self.s = s
        self.t = t
        self.id = id
        self.zOffset = None
        self.valid_length = None
        self.orientation = orientation
        self.validity = []


class Object:

    def __init__(self):
        self.t = None
        self.z_offset = None
        self.type = None
        self.valid_length = None
        self.orientation = None
        self.subtype = None
        self.dynamic = None
        self.hdg = None
        self.name = None
        self.pitch = None
        self.id = None
        self.roll = None
        self.height = None
        self.s = None
        self.length = None
        self.width = None
        self.radius = None
        self.material = []
        self.repeat = []
        self.parking_space = None
        self.outline = None
        self.outlines = None
        self.validity = []
        self.borders = None
        self.markings = None


class ObjectParkingSpace:

    def __init__(self):
        self.access = None
        self.restrictions = None
