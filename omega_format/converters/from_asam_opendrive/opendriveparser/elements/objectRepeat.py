class ObjectRepeat:

    def __init__(self, s=None, length=None, distance=None, t_start=None, t_end=None, height_start=None,
                 height_end=None):
        self.s = float(s)
        self.length = float(length)
        self.distance = float(distance)
        self.t_start = float(t_start)
        self.t_end = float(t_end)
        self.height_start = float(height_start)
        self.height_end = float(height_end)
        self.z_offset_start = None
        self.z_offset_end = None
        self.width_start = None
        self.width_end = None
        self.length_start = None
        self.length_end = None
        self.radius_start = None
        self.radius_end = None
