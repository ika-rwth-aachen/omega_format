from .roadLink import Link
from .roadPlanView import RoadPlanView as PlanView
from .roadElevationProfile import ElevationProfile
from .roadLateralProfile import LateralProfile
from .roadLanes import Lanes
from .roadSurface import RoadSurface as Surface


class Road:

    def __init__(self):
        self.name = None
        self.length = None
        self.id = None
        self.junction = None
        self.rule = None
        self.link = Link()
        self.type = []
        self.plan_view = PlanView()
        self.elevation_profile = ElevationProfile()
        self.lateral_profile = LateralProfile()
        self.lanes = Lanes()
        self.surface = Surface()
        self.objects = None
        self.signals = None
