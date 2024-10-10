class PhysicalPosition:

    def __init__(self):
        self.position_road = None
        self.position_inertial = None


class PositionRoad:

    def __init__(self):
        self.road_id = None
        self.s = None
        self.t = None
        self.z_offset = None
        self.h_offset = None
        self.pitch = None
        self.roll = None


class PositionInertial:

    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.hdg = None
        self.pitch = None
        self.roll = None
