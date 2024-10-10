class RoadSurface:

    def __init__(self):
        self.crg = []


class RoadSurfaceCrg:

    def __init__(self, file=None, s_start=None, s_end=None, orientation=None, mode=None, purpose=None, s_offset=None, t_offset=None,
                 z_offset=None, z_scale=None, h_offset=None):
        self.file = file
        self.s_start = s_start
        self.s_end = s_end
        self.orientation = orientation
        self.mode = mode
        self.purpose = purpose
        self.s_offset = s_offset
        self.t_offset = t_offset
        self.z_offset = z_offset
        self.z_scale = z_scale
        self.h_offset = h_offset
