class RoadPlanView:

    def __init__(self):
        self.geometry = []


class RoadGeometry:

    def __init__(self):
        self.s = None
        self.x = None
        self.y = None
        self.hdg = None
        self.length = None

        self.line = RoadLine()
        self.spiral = RoadSpiral()
        self.arc = RoadArc()
        self.poly3 = RoadPoly3()
        self.param_poly3 = RoadParamPoly3()


class RoadLine:
    """ """
    def __init__(self, line=None):
        # according to documentation line actually does not contain any additional information
        self.line = line


class RoadSpiral:
    def __init__(self, curv_start=None, curv_end=None):
        self.curv_start = curv_start
        self.curv_end = curv_end


class RoadArc:
    def __init__(self, curvature=None):
        self.curvature = curvature


class RoadPoly3:
    def __init__(self, a=None, b=None, c=None, d=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class RoadParamPoly3:
    def __init__(self, a_u=None, b_u=None, c_u=None, d_u=None, a_v=None, b_v=None, c_v=None, d_v=None,
                 p_range=None):
        self.a_u = a_u
        self.b_u = b_u
        self.c_u = c_u
        self.d_u = d_u
        self.a_v = a_v
        self.b_v = b_v
        self.c_v = c_v
        self.d_v = d_v
        self.p_range = p_range
