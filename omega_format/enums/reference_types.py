from enum import Enum, IntEnum
import warnings
import importlib
from typing import Union


class ReferenceTypesSpecification(Enum):
    FORMAT_VERSION = importlib.metadata.version('omega-format')


class RoadLocation(IntEnum):
        UNKNOWN = 0
        URBAN = 1
        NON_URBAN = 2
        HIGHWAY = 3

        @classmethod
        def _missing_(cls, value):
            if value=="TODO":
                return cls.UNKNOWN
            else:
                return super()._missing_(cls, value)


class LaneType(IntEnum):
    UNKNOWN = 0
    DRIVING = 1
    SHOULDER = 2
    BUS_LANE = 3
    BICYCLE_LANE = 4
    ON_RAMP = 5
    OFF_RAMP = 6
    SHARED_WALKWAY = 7
    WALKWAY = 8
    CARPOOL_LANE = 9
    BUS_BICYCLE_LANE = 10
    BUS_BAY = 11
    VEHICLE_TURNOUT = 12
    KEEPOUT = 13
    RAIL = 14
    VEGETATION = 15
    FREESPACE = 16

    @classmethod
    def _missing_(cls, value):
        if value=="TODO":
            return cls.UNKNOWN
        else:
            return super()._missing_(cls, value)

class LaneSubType(IntEnum):
    UNKNOWN = 0
    BRIDGE = 1
    TUNNEL = 2

    @classmethod
    def _missing_(cls, value):
        if value=="TODO":
            return cls.UNKNOWN
        else:
            return super()._missing_(cls, value)

class LaneClass(IntEnum):
    NONE = 0
    INTERSECTION = 1
    ROUNDABOUT = 2


class BoundaryType(IntEnum):
    UNKNOWN = 0
    SOLID = 1
    DASHED = 2
    SOLID_SOLID = 3
    SOLID_DASHED = 4
    DASHED_SOLID = 5
    DASHED_CHANGE_DIRECTION_LANE = 6
    HAPTIC_ACOUSTIC = 7
    STUDS = 8
    REFLECTOR_GUIDING_LAMPS = 9
    GUARD_RAIL = 10
    GUARD_RAIL_ACCIDENT_PROTECTION = 11
    CONCRETE_BARRIER = 12
    REFLECTOR_POSTS = 13
    SAFETY_BEACONS = 14
    DIVIDER = 15
    NOISE_PROTECTION_WALL = 16
    CURB = 17
    ANTI_GLARE_SCREEN = 18
    FENCE = 19
    VIRTUAL = 20
    MISC = 21
    STRUCTURAL_OBJECT = 22

    @classmethod
    def _missing_(cls, value):
        if value=="TODO":
            return cls.UNKNOWN
        else:
            return super()._missing_(cls, value)

class BoundarySubType(IntEnum):
    UNKNOWN = 0
    THIN = 1
    THICK = 2
    METAL = 3
    WOODEN = 4
    
    @classmethod
    def _missing_(cls, value):
        if value=="TODO":
            return cls.UNKNOWN
        else:
            return super()._missing_(cls, value)


class BoundaryColor(IntEnum):
    UNKNOWN = 0
    WHITE = 1
    YELLOW = 2
    GREEN = 3
    RED = 4


class BoundaryCondition(IntEnum):
    UNKNOWN = 0
    FINE = 1
    CORRUPTED_1_BAD_SURFACE = 2  # bad surface
    CORRUPTED_2_FADED = 3  # faded


class SignType(str, Enum):
    UNKNOWN = '0'
    DS_GENERAL = '101'
    DS_DOMESTIC_ANIMAL_CROSSING = '101-12'
    DS_HORSE_RIDER = '101-13'
    DS_FALLING_ROCKS = '101-15'
    DS_LOW_FLYING_AIRCRAFT = '101-20'
    DS_GRAVEL = '101-52'
    DS_CLEARANCE = '101-54'
    CROSSING = '102'
    DS_BEND_LEFT = '103-10'
    DS_BEND_RIGHT = '103-20'
    DS_DOUBLE_BEND_LEFT_FIRST = '105-10'
    DS_DOUBLE_BEND_RIGHT_FIRST = '105-20'
    DS_RIGHT_DOWNWARDS = '108'
    DS_RIGHT_UPWARDS = '110'
    DS_TWO_BUMP = '112'
    DS_SNOW = '113'
    DS_SLIPPERY_ROAD = '114'
    DS_WIND_FROM_SIDE = '117-10'
    DS_ROAD_NARROW_BOTH_SIDES = '120'
    DS_ROAD_NARROW_RIGHT_SIDE = '121-10'
    DS_ROAD_NARROW_LEFT_SIDE = '121-20'
    DS_ROAD_WORK = '123'
    DS_TRAFFIC_JAM = '124'
    DS_TWO_WAY_TRAFFIC = '125'
    DS_RIVER_BANK = '129'
    DS_TRAFFIC_LIGHT = '131'
    DS_PEDESTRIAN = '133-10'
    DS_PEDESTRIAN_CROSSING = '134'
    DS_CHILDREN = '136-10'
    DS_BICYCLE_CROSSING = '138'
    DS_ANIMAL_CROSSING = '142-10'
    DS_BUSES = '145'
    DS_AMPHIBIA = '145-15'
    DS_DRAW_BRIDGE = '145-54'
    DS_TRAIN_CROSS_WITH_BARRIER = '150'
    DS_TRAIN_CROSS_WITHOUT_BARRIER = '151'
    DS_TRAIN_CROSS = '201-50'
    GIVE_WAY = '205'
    STOP_GIVE_WAY = '206'
    ONCOMING_PRIORITY_GIVEAWAY = '208'
    MANDATORY_TURN_RIGHT = '209' #209-20 (wird automatisch genommen und ist in ordnung)
    MANDATORY_TURN_LEFT = '209-10'
    MANDATORY_STRAIGHT = '209-30'
    MANDATORY_PASSING_HERE_LEFT = '211-10'
    MANDATORY_PASSING_HERE_RIGHT ='211'
    PRESCRIBED_DIRECTION_STRAIGHT_RIGHT = '214'
    MANDATORY_PASSING_STRAIGHT_LEFT = '214-10'
    MANDATORY_PASSING_LEFT_RIGHT = '214-30'
    ROUNDABOUT_SIGN = '215'
    ONE_WAY_STREET_LEFT = '220-10'
    ONE_WAY_STREET_RIGHT = '220-20'
    PRESCRIBED_PASSING_RIGHT = '222' # is also 222-20
    PRESCRIBED_PASSING_LEFT = '222-10'
    DRIVING_EMERGENCY_LANE_ALLOWED = '223-1'
    DRIVING_EMERGENCY_LANE_CANCELLED = '223-2'
    DRIVING_EMERGENCY_LANE_MERGE_LEFT = '223-3'
    BUS_STOP = '224'
    WALKWAY = '239'
    PEDESTRIAN_BICYCLE_LANE = '240'
    PEDESTRIAN_BICYCLE_LANE_VERTICAL = '241'
    BICYCLE_STREET_END = '244_2'
    NO_VEHICLES_ALLOWED = '250'
    MOTORS_PROHIBITED = '251'
    NO_CYCLING = '254'
    MOTORCYCLES_PROHIBITED = '255'
    PEDESTRIANS_PROHIBITED = '259'
    ALL_VEHICLES_PROHIBITED = '260'
    HAZARDOUS_PROHIBITED = '261'
    WEIGHT_LIMIT = '262'
    WIDTH_LIMIT = '264'
    HEIGHT_LIMIT = '265'
    NO_ENTRY = '267'
    ENVIRONMENTAL_ZONE_START_OF = '270-1'
    ENVIRONMENTAL_ZONE_END_OF = '270-2'
    U_TURN_PROHIBITED = '272'
    ZONE_30_START = '274-1'
    ZONE_20_START = '274-1-20'
    ZONE_30_END = '274-2'
    ZONE_20_END = '274-2-20'
    MAXIMUM_SPEED_5 = '274-5'
    MAXIMUM_SPEED_10 = '274-10'
    MAXIMUM_SPEED_20 = '274-20'
    MAXIMUM_SPEED_30 = '274-30'
    MAXIMUM_SPEED_40 = '274-40'
    MAXIMUM_SPEED_50 = '274-50'
    MAXIMUM_SPEED_60 = '274-60'
    MAXIMUM_SPEED_70 = '274-70'
    MAXIMUM_SPEED_80 = '274-80'
    MAXIMUM_SPEED_90 = '274-90'
    MAXIMUM_SPEED_100 = '274-100'
    MAXIMUM_SPEED_110 = '274-110'
    MAXIMUM_SPEED_120 = '274-120'
    MAXIMUM_SPEED_130 = '274-130'
    MINIMUM_SPEED_LIMIT = '275'
    NO_PASSING_SIGN = '276'
    NO_PASSING_TRUCK = '277'
    MAXIMUM_SPEED_5_CANCELLED = '278-5'
    MAXIMUM_SPEED_10_CANCELLED = '278-10'
    MAXIMUM_SPEED_20_CANCELLED = '278-20'
    MAXIMUM_SPEED_30_CANCELLED = '278-30'
    MAXIMUM_SPEED_40_CANCELLED = '278-40'
    MAXIMUM_SPEED_50_CANCELLED = '278-50'
    MAXIMUM_SPEED_60_CANCELLED = '278-60'
    MAXIMUM_SPEED_70_CANCELLED = '278-70'
    MAXIMUM_SPEED_80_CANCELLED = '278-80'
    MAXIMUM_SPEED_90_CANCELLED = '278-90'
    MAXIMUM_SPEED_100_CANCELLED = '278-100'
    MAXIMUM_SPEED_110_CANCELLED = '278-110'
    MAXIMUM_SPEED_120_CANCELLED = '278-120'
    MAXIMUM_SPEED_130_CANCELLED = '278-130'
    MINIMUM_SPEED_LIMIT_CANCELLATION = '279'
    WITHDRAWAL_NO_PASSING_SIGN = '280'
    WITHDRAWAL_NO_PASSING_TRUCK = '281'
    GENERAL_WITHDRAWAL = '282'
    NO_PARKING = '283'
    NO_PARKING_START = '283-10'
    NO_PARKING_END = '283-20'
    NO_PARKING_MID = '283-30'
    RESTRICTED_PARKING = '286'
    RESTRICTED_PARKING_START = '286-10'
    RESTRICTED_PARKING_END = '286-20'
    RESTRICTED_PARKING_MID = '286-30'
    PARKING_RESTRICTED_ZONE_START = '290-1'
    PARKING_RESTRICTED_ZONE_END = '290-2'
    PRIORITY = '301'
    PRIORITY_ROAD = '306'
    PRIORITY_ROAD_END_OF = '307'
    ONCOMING_PRIORITY = '308'
    CITY_LIMIT_START_OF = '310'
    CITY_LIMIT_START_END_OF = '311'
    PARKING = '314'
    PARKING_ZONE_START = '314-1'
    PARKING_ZONE_END = '314-2'
    PARKING_ON_SIDEWALK_HALF_RIGHT_CENTER = '315-58'
    PARKING_ON_SIDEWALK_HALF_RIGHT_START = '315-56'
    TRAFFIC_CALM_AREA_START = '325-1'
    TRAFFIC_CALM_AREA_END = '325-2'
    TRAFFIC_CALMING_ZONE_END_OF = '326'
    TUNNEL = '327'
    BREAKDOWN_BAY = '328'
    MOTORWAY_START_OF = '330-1'
    MOTORWAY_END_OF = '330-2'
    EXPRESSWAY_START_OF = '331-1'
    EXPRESSWAY_END_OF = '331-2'
    HIGHWAY_EXIT_ARROW = '333'
    PEDESTRIAN_CROSSING_RIGHT = '350-10'
    PEDESTRIAN_CROSSING_LEFT = '350-20'
    ONE_WAY_STREET = '353'
    DEAD_END = '357'
    DEAD_END_CYCLISTS_AND_PEDESTRIANS_CAN_PASS = '357-50'
    DEAD_END_PEDESTRIANS_CAN_PASS = '357-51'
    REFULING = '365'
    ADVISORY_SPEED_LIMIT = '380'
    ADVISORY_SPEED_LIMIT_CANCELLATION = '381'
    SMALL_CITY_LIMIT_START_OF = '385'
    TOLL = '391'
    EXIT_NUMBER = '406'
    MOTORWAY_RIGHT = '430-20'
    DIRECTIONAL_SIGN = '449'
    HIGHWAY_EXIT_300 = '450-52'
    HIGHWAY_EXIT_200 = '450-51'
    HIGHWAY_EXIT_100 = '450-52'
    DIVERSION_LEFT = '454-10'
    DIVERSION_RIGHT = '454-20'
    DIVERSION_START = '457-1'
    DIVERSION_END = '457-2'
    LANES_CHANGE_LEFT = '501-10'
    LANES_CHANGE_RIGHT = '501-20'
    LANES_STRAIGHT = '521-30'
    LANES_END_RIGHT = '531-10'
    LANES_END_LEFT = '531-20'
    LANES_NEW_LEFT = '541-10'
    LANES_NEW_RIGHT = '541-20'
    LANES_ADD_RIGHT = '550-20'
    LANES_ADD_LEFT = '551-20'
    GUIDE_PLATE = '626-30'
    LEFT_ARROW = '1000-10'
    LEFT_BEND_ARROW = '1000-11'
    RIGHT_ARROW = '1000-20'
    RIGHT_BEND_ARROW = '1000-21'
    CROSSING_BICYCLE_LEFT_RIGHT = '1000-32'
    DISTANCE_FOR = '1001-30'
    MAIN_ROAD_DOWN_LEFT = '1002-10'
    MAIN_ROAD_UP_LEFT = '1002-11'
    MAIN_ROAD_DOWN_RIGHT = '1002-20'
    MAIN_ROAD_UP_RIGHT = '1002-21'
    DISTANCE_IN = '1004-31'
    STOP_IN = '1004-32'
    PICTURE = '1006-31' # Unfallgefahr
    TEXT = '1007'
    TRUCK = '1010-51'
    BUS = '1010-57'
    CAR = '1010-58'
    TRACTOR = '1010-61'
    MOTORCYCLE = '1010-62'
    TRAILER = '1011-59'
    SCHOOL = '1012-50'
    RESIDENTS_FREE = '1020-30'
    CYCLISTS_ARE_ALLOWED = '1022-10'
    MOTORCYCLE_ALLOWED = '1022-12'
    TIME_16_18 = '1040-30'
    TIME_NOISE = '1040-35'
    TRACTORS_MAY_BE_PASSED = '1049-11'
    HAZARDOUS = '1052-30'
    PARKING_WITH_TICKET = '1053-31'
    WEIGHT = '1053-33'
    RAIN = '1053-35'
    TL_REGULAR = '2000-1'
    TL_ARROW_STRAIGHT = '2000-2'
    TL_ARROW_RIGHT = '2000-3'
    TL_ARROW_LEFT = '2000-4'
    TL_ARROW_STRAIGHT_RIGHT = '2000-5'
    TL_ARROW_STRAIGHT_LEFT = '2000-6'
    TL_PEDESTRIAN = '2000-7'
    TL_BICYCLE = '2000-8'
    TL_PEDESTRIAN_BICYCLE = '2000-9'
    LIGHT_SINGLE = '2000-10'
    TL_RED_AMBER = '2000-11'
    LANE_LIGHT = '2000-12'
    BUS_LIGHT = '2000-13'
    SWITCHABLE = '3000-1'
    BARRIER = '4000-1'

    @classmethod
    def _missing_(cls, value):
        new_value = None
        if '_' in value:
            new_value = value.replace('_','-')
        elif ('(') in value:
            new_value = value.split('(')[0]
        elif '.' in value:
            new_value = value.replace('.', '-')
        elif int(value[-1]==0):
            new_value =  cls(value[:-1])
        elif '-' in value:
            new_value = value.split('-')[0]
        if new_value is not None:
            warnings.warn(f'Sign Type {value} unkown: interpreted as Sign Type {new_value}!')
            return cls(new_value)
        else:
            return super()._missing_(cls, value)


class SignSizeClass(IntEnum):
    UNKNOWN = 0
    SMALL = 1
    MIDDLE = 2
    LARGE = 3


class FlatMarkingType(IntEnum):
    UNKNOWN = 0
    NOTICE_ARROW = 1
    ZIG_ZAG = 2
    KEEPOUT_AREA = 3
    ARROW_LEFT = 4
    ARROW_RIGHT = 5
    ARROW_LEFT_RIGHT = 6
    ARROW_LEFT_STRAIGHT = 7
    ARROW_RIGHT_STRAIGHT = 8
    ARROW_LEFT_STRAIGHT_RIGHT = 9
    ARROW_STRAIGHT = 10
    VEHICLEFRONT = 11
    TRUCK = 12
    BICYCLE = 13
    DELIVERYBIKE = 14
    PEDESTRIAN = 15
    HORSERIDER = 16
    CATTLEDRIVE = 17
    TRAM = 18
    BUS = 19
    VEHICLE = 20
    VEHICLEMULTIPLEPASSENGERS = 21
    PKWWITHTRAILER = 22
    TRUCKWITHTRAILER = 23
    MOBILEHOME = 24
    TRACTOR = 25
    MOTORCYCLE = 26
    MOPED = 27
    ELECTRICBICYCLE = 28
    ESCOOTER = 29
    CARRIAGE = 30
    SNOWICE = 31
    ROCKFALL = 32
    GRAVEL = 33
    MOVABLEBRIDGE = 34
    SHORE = 35
    CROSSWALK = 36
    AMPHIBIAN = 37
    AVENUE = 38
    PLANE = 39
    ELECTRICALVEHICLE = 40
    CARSHARING = 41

    @classmethod
    def _missing_(cls, value):
        if value=="TODO":
            return cls.UNKNOWN
        else:
            return super()._missing_(cls, value)


class FlatMarkingColor(IntEnum):
    UNKNOWN = 0
    WHITE = 1
    YELLOW = 2
    GREEN = 3
    RED = 4
    BLUE = 5


class FlatMarkingCondition(IntEnum):
    UNKNOWN = 0
    FINE = 1
    CORRUPTED_1_OLD_VISIBIBLE = 2
    CORRUPTED_2_FADED = 3


class LateralMarkingType(IntEnum):
    UNKNOWN = 0
    STOP_LINE = 1
    HOLD_LINE = 2
    PEDESTRIAN_CROSSING_LINE = 3
    BICYCLE_CROSSING = 4
    CROSSWALK = 5
    REFLECTORS_LAMPS = 6
    SHARK_TOOTH = 7


class LateralMarkingColor(IntEnum):
    UNKNOWN = 0
    WHITE = 1
    YELLOW = 2
    GREEN = 3
    RED = 4
    BLUE = 5


class LateralMarkingCondition(IntEnum):
    UNKNOWN = 0
    FINE = 1
    CORRUPTED_1_CORRUPTED = 2
    CORRUPTED_2_FADED = 3


class SurfaceMaterial(IntEnum):
    UNKNOWN = 0
    ASPHALT = 1
    CONCRETE = 2
    BRICK = 3
    GRAVEL = 4


class SurfaceColor(IntEnum):
    UNKNOWN = 0
    WHITE = 1
    GREEN = 3
    RED = 4
    ANTHRACITE = 6
    BROWN = 7


class SurfaceCondition(IntEnum):
    NO_VALUE = 0
    FINE = 1
    CRACKS = 2
    BITUMEN = 3
    POT_HOLES = 4
    RUTS = 5
    DAMAGED = 6


class RoadObjectType(IntEnum):
    UNKNOWN = 0
    STREET_LAMP = 1
    TRAFFIC_ISLAND = 2
    ROUNDABOUT_CENTER = 3
    PARKING = 4
    CROSSING_AID = 5
    SPEED_BUMP = 6
    POT_HOLE = 7
    REFLECTOR = 8
    STUD = 9
    BOLLARD = 10
    CRASH_ABSORBER = 11
    BITUMEN = 12
    MANHOLE_COVER = 13
    GRATING = 14
    RUT = 15
    PUDDLE = 16
    MISC = 17


class StructuralObjectType(IntEnum):
    NOT_DECLARED = 0
    VEGETATION = 1
    BUILDING = 2
    BUS_SHELTER = 3
    TUNNEL = 4
    BRIDGE = 5
    FENCE = 6
    BENCH = 7
    ROAD_WORK = 8
    BODY_OF_WATER = 9
    GARAGE = 10
    BILLBOARD = 11
    ADVERTISING_PILLAR = 12
    PHONE_BOX = 13
    POST_BOX = 14
    OVERHEAD_STRUCTURE = 15


class LayerFlag(IntEnum):
    PERMANENT_GENERAL = 0
    ROAD_NETWORK_TRAFFIC_GUIDANCE_OBJECT = 1
    ROADSIDE_STRUCTURE = 2
    TEMPORARY_MODIFICATION = 3
    DYNAMIC_OBJECT = 4
    ENVIRONMENTAL_CONDITION = 5
    DIGITAL_INFORMATION = 6


class RoadUserVehicleLights(IntEnum):
    UNKNOWN = -1
    OFF = 0
    ON = 1

class RoadUserType(IntEnum):
    REGULAR = 0
    CAR = 1
    TRUCK = 2
    BUS = 3
    MOTORCYCLE = 4
    BICYCLE = 5
    PEDESTRIAN = 6
    PUSHABLE_PULLABLE = 7
    WHEELCHAIR = 8
    PERSONAL_MOBILITY_DEVICE = 9
    TRAILER = 10
    FARMING = 11
    RAIL = 12
    CARRIAGE = 13

    @staticmethod
    def get_subtype(_type, subtype_int):
        try:
            subtype = globals()['RoadUserSubType'+_type.name]
        except KeyError:
            subtype = RoadUserSubTypeGeneral
        return subtype(subtype_int)

class RoadUserSubTypeGeneral(IntEnum):
    REGULAR = 0
    EMERGENCY = 1
    CONSTRUCTION = 2


class RoadUserSubTypeTRUCK(IntEnum):
    REGULAR = 0
    EMERGENCY = 1
    CONSTRUCTION = 2
    STREET_CLEANING = 3


class RoadUserSubTypeBUS(IntEnum):
    REGULAR = 0
    EMERGENCY = 1
    CONSTRUCTION = 2
    TROLLEY_BUS = 3
    BENDY_BUS = 4


class RoadUserSubTypeMOTORCYCLE(IntEnum):
    REGULAR = 0
    EMERGENCY = 1
    CONSTRUCTION = 2
    WITH_RIDER = 3
    WITHOUT_RIDER = 4


class RoadUserSubTypeBICYCLE(IntEnum):
    REGULAR = 0
    EMERGENCY = 1
    CONSTRUCTION = 2
    WITH_RIDER = 3
    WITHOUT_RIDER = 4


class RoadUserSubTypePEDESTRIAN(IntEnum):
    REGULAR = 0
    EMERGENCY = 1
    CONSTRUCTION = 2
    CHILD = 3
    ADULT = 4


class RoadUserSubTypeWHEELCHAIR(IntEnum):
    REGULAR = 0
    EMERGENCY = 1
    CONSTRUCTION = 2
    WITH_RIDER = 3
    WITHOUT_RIDER = 4


class RoadUserSubTypePERSONAL_MOBILITY_DEVICE(IntEnum):
    REGULAR = 0
    EMERGENCY = 1
    CONSTRUCTION = 2
    WITH_RIDER = 3
    WITHOUT_RIDER = 4

class RoadUserSubTypeTRAILER(IntEnum):
    REGULAR = 0
    EMERGENCY = 1
    CONSTRUCTION = 2
    CAR_TRAILER = 3
    CARAVAN = 4
    TRUCK_TRAILER = 5
    TRAIN_TRAILER = 6
    BENDY_BUS_TRAILER = 7


RoadUserSubType = Union[RoadUserSubTypeGeneral,RoadUserSubTypeBICYCLE,RoadUserSubTypeBUS,RoadUserSubTypeMOTORCYCLE,RoadUserSubTypePEDESTRIAN,RoadUserSubTypePERSONAL_MOBILITY_DEVICE,RoadUserSubTypeTRAILER,RoadUserSubTypeTRUCK,RoadUserSubTypeWHEELCHAIR]

class MiscObjectType(IntEnum):
    UNKNOWN = 0
    ANIMAL = 1
    PLAY_EQUIPMENT = 2
    MISC = 3

    @classmethod
    def _missing_(cls, value):
        if value=="TODO":
            return cls.UNKNOWN
        else:
            return super()._missing_(cls, value)

class MiscObjectSubType(IntEnum):
    UNKNOWN = 0
    DOG = 1
    CAT = 2
    HORSE = 3
    BIRD = 4
    WILD = 5

    @classmethod
    def _missing_(cls, value):
        if value=="TODO":
            return cls.UNKNOWN
        else:
            return super()._missing_(cls, value)

class StateValue(IntEnum):
    UNKNOWN = 0
    GREEN = 1
    AMBER = 2
    RED = 3
    RED_AMBER = 4
    FLASHING_AMBER = 5
    FLASHING_RED = 6
    GREEN_ARROW = 7
    RED_CROSS = 8
    AMBER_DIAGONAL_ARROW_RIGHT = 9
    AMBER_DIAGONAL_ARROW_LEFT = 10
    ACTIVE = 11
    INACTIVE = 12
    BUS_STOP = 13
    BUS_STRAIGHT = 14
    BUS_RIGHT = 15
    BUS_LEFT = 16
    BUS_STOP_EXPECTED = 17
    BUS_YIELD = 18
    BUS_WILL_SWITCH = 19

class WeatherSource(IntEnum):
    UNKNOWN = 0
    DWD = 1
    EXTERNAL_SENSOR = 2

class Precipitation(IntEnum):
    NO_RAIN = 0
    LIGHT_RAIN = 1
    MODERATE_RAIN = 2
    HEAVY_RAIN = 3
    EXTREMELY_HEAVY_RAIN = 4
    LIGHT_SNOW = 5
    MODERATE_SNOW = 6
    HEAVY_SNOW = 7
    LEFT_OVER_ON_GROUND = 8
    OLD_LEFT_OVER_ON_GROUND = 9
    OLD_LEFT_OVER_ON_GROUND_ONLY_LIQUID = 10

class Wind(IntEnum):
    CALM = 0
    LIGHT_AIR = 1
    LIGHT_BREEZE = 2
    GENTLE_BREEZE = 3
    MODERATE_BREEZE = 4
    FRESH_BREEZE = 5
    STRONG_BREEZE = 6
    NEAR_GALE = 7
    GALE = 8
    STRONG_GALE = 9
    STORM = 10
    VIOLENT_STORM = 11
    HURRICANE = 12

class GustOfWind(IntEnum):
    NO_GUSTS_OF_WIND = 0
    GUST_OF_WIND = 1
    SQUALL = 2
    HEAVY_SQUALL = 3
    VIOLENT_SQUALL = 4
    GALE_FORCE_WINDS = 5
    SEVERE_GALE_FORCE_WINDS = 6


class RoadConditionSurfaceCondition(IntEnum):
    BARE = 0
    MOIST = 1
    WET = 2
    WET_WITH_BODY_OF_WATER = 21
    SLIPPERINESS = 3
    BLACK_ICE = 4
    PARTLY_SNOW = 5
    SNOW_COVERED = 6
    COMPACTED_SNOW = 7
    ICE_COVERED_SNOW = 8
    UNKNOWN = 9

class RoadConditionMaintenanceStatus(IntEnum):
    UNKNOWN = 0
    UNTREATED = 1
    SALTED = 2
    DIRTY = 3
    GRIT = 4
