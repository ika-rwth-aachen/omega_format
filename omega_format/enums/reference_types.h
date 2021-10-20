#pragma once
// auto-generated file from .py original

enum class VVMBoundaryColor {
  UNKNOWN = 0,
  WHITE = 1,
  YELLOW = 2,
  GREEN = 3,
  RED = 4
};

enum class VVMBoundaryCondition {
  UNKNOWN = 0,
  FINE = 1,
  CORRUPTED_1_BAD_SURFACE = 2,
  CORRUPTED_2_FADED = 3
};

enum class VVMBoundarySubType {
  TODO = 0,
  THIN = 1,
  THICK = 2,
  METAL = 3,
  WOODEN = 4
};

enum class VVMBoundaryType {
  TODO = 0,
  SOLID = 1,
  DASHED = 2,
  SOLID_SOLID = 3,
  SOLID_DASHED = 4,
  DASHED_SOLID = 5,
  DASHED_CHANGE_DIRECTION_LANE = 6,
  HAPTIC_ACOUSTIC = 7,
  STUDS = 8,
  REFLECTOR_GUIDING_LAMPS = 9,
  GUARD_RAIL = 10,
  GUARD_RAIL_ACCIDENT_PROTECTION = 11,
  CONCRETE_BARRIER = 12,
  REFLECTOR_POSTS = 13,
  SAFETY_BEACONS = 14,
  DIVIDER = 15,
  NOISE_PROTECTION_WALL = 16,
  CURB = 17,
  ANTI_GLARE_SCREEN = 18,
  FENCE = 19,
  VIRTUAL = 20,
  MISC = 21,
  STRUCTURAL_OBJECT = 22
};

enum class VVMFlatMarkingColor {
  UNKNOWN = 0,
  WHITE = 1,
  YELLOW = 2,
  GREEN = 3,
  RED = 4,
  BLUE = 5
};

enum class VVMFlatMarkingCondition {
  UNKNOWN = 0,
  FINE = 1,
  CORRUPTED_1_OLD_VISIBIBLE = 2,
  CORRUPTED_2_FADED = 3
};

enum class VVMFlatMarkingType {
  TODO = 0,
  NOTICE_ARROW = 1,
  ZIG_ZAG = 2,
  KEEPOUT_AREA = 3,
  ARROW_LEFT = 4,
  ARROW_RIGHT = 5,
  ARROW_LEFT_RIGHT = 6,
  ARROW_LEFT_STRAIGHT = 7,
  ARROW_RIGHT_STRAIGHT = 8,
  ARROW_LEFT_STRAIGHT_RIGHT = 9,
  ARROW_STRAIGHT = 10,
  VEHICLEFRONT = 11,
  TRUCK = 12,
  BICYCLE = 13,
  DELIVERYBIKE = 14,
  PEDESTRIAN = 15,
  HORSERIDER = 16,
  CATTLEDRIVE = 17,
  TRAM = 18,
  BUS = 19,
  VEHICLE = 20,
  VEHICLEMULTIPLEPASSENGERS = 21,
  PKWWITHTRAILER = 22,
  TRUCKWITHTRAILER = 23,
  MOBILEHOME = 24,
  TRACTOR = 25,
  MOTORCYCLE = 26,
  MOPED = 27,
  ELECTRICBICYCLE = 28,
  ESCOOTER = 29,
  CARRIAGE = 30,
  SNOWICE = 31,
  ROCKFALL = 32,
  GRAVEL = 33,
  MOVABLEBRIDGE = 34,
  SHORE = 35,
  CROSSWALK = 36,
  AMPHIBIAN = 37,
  AVENUE = 38,
  PLAIN = 39,
  ELECTRICALVEHICLE = 40,
  CARSHARING = 41
};

enum class VVMGustOfWind {
  NO_GUSTS_OF_WIND = 0,
  GUST_OF_WIND = 1,
  SQUALL = 2,
  HEAVY_SQUALL = 3,
  VIOLENT_SQUALL = 4,
  GALE_FORCE_WINDS = 5,
  SEVERE_GALE_FORCE_WINDS = 6
};

enum class VVMLaneClass {
  NONE = 0,
  INTERSECTION = 1,
  ROUNDABOUT = 2
};

enum class VVMLaneSubType {
  TODO = 0,
  BRIDGE = 1,
  TUNNEL = 2
};

enum class VVMLaneType {
  TODO = 0,
  DRIVING = 1,
  SHOULDER = 2,
  BUS_LANE = 3,
  BICYCLE_LANE = 4,
  ON_RAMP = 5,
  OFF_RAMP = 6,
  SHARED_WALKWAY = 7,
  WALKWAY = 8,
  CARPOOL_LANE = 9,
  BUS_BICYCLE_LANE = 10,
  BUS_BAY = 11,
  VEHICLE_TURNOUT = 12,
  KEEPOUT = 13,
  RAIL = 14,
  VEGETATION = 15,
  FREESPACE = 16
};

enum class VVMLateralMarkingColor {
  UNKNOWN = 0,
  WHITE = 1,
  YELLOW = 2,
  GREEN = 3,
  RED = 4,
  BLUE = 5
};

enum class VVMLateralMarkingCondition {
  UNKNOWN = 0,
  FINE = 1,
  CORRUPTED_1_CORRUPTED = 2,
  CORRUPTED_2_FADED = 3
};

enum class VVMLateralMarkingType {
  UNKNOWN = 0,
  STOP_LINE = 1,
  HOLD_LINE = 2,
  PEDESTRIAN_CROSSING_LINE = 3,
  BICYCLE_CROSSING = 4,
  CROSSWALK = 5,
  REFLECTORS_LAMPS = 6,
  SHARK_TOOTH = 7
};

enum class VVMLayerFlag {
  PERMANENT_GENERAL = 0,
  ROAD_NETWORK_TRAFFIC_GUIDANCE_OBJECT = 1,
  ROADSIDE_STRUCTURE = 2,
  TEMPORARY_MODIFICATION = 3,
  DYNAMIC_OBJECT = 4,
  ENVIRONMENTAL_CONDITION = 5,
  DIGITAL_INFORMATION = 6
};

enum class VVMMiscObjectSubType {
  TODO = 0,
  DOG = 1,
  CAT = 2,
  HORSE = 3,
  BIRD = 4,
  WILD = 5
};

enum class VVMMiscObjectType {
  TODO = 0,
  ANIMAL = 1,
  PLAY_EQUIPMENT = 2,
  MISC = 3
};

enum class VVMPrecipitation {
  NO_RAIN = 0,
  LIGHT_RAIN = 1,
  MODERATE_RAIN = 2,
  HEAVY_RAIN = 3,
  EXTREMELY_HEAVY_RAIN = 4,
  LIGHT_SNOW = 5,
  MODERATE_SNOW = 6,
  HEAVY_SNOW = 7,
  LEFT_OVER_ON_GROUND = 8,
  OLD_LEFT_OVER_ON_GROUND = 9,
  OLD_LEFT_OVER_ON_GROUND_ONLY_LIQUID = 10
};

enum class VVMRecorderNumber {
  AVL = 1,
  IKA = 2,
  DLR = 3
};

class VVMReferenceTypesSpecification {
public:
  const char* FORMAT_VERSION = "v3.1";
};

enum class VVMRoadConditionMaintenanceStatus {
  UNKNOWN = 0,
  UNTREATED = 1,
  SALTED = 2,
  DIRTY = 3,
  GRIT = 4
};

enum class VVMRoadConditionSurfaceCondition {
  BARE = 0,
  MOIST = 1,
  WET = 2,
  WET_WITH_BODY_OF_WATER = 21,
  SLIPPERINESS = 3,
  BLACK_ICE = 4,
  PARTLY_SNOW = 5,
  SNOW_COVERED = 6,
  COMPACTED_SNOW = 7,
  ICE_COVERED_SNOW = 8,
  UNKNOWN = 9
};

enum class VVMRoadLocation {
  TODO = 0,
  URBAN = 1,
  NON_URBAN = 2,
  HIGHWAY = 3
};

enum class VVMRoadObjectType {
  UNKNOWN = 0,
  STREET_LAMP = 1,
  TRAFFIC_ISLAND = 2,
  ROUNDABOUT_CENTER = 3,
  PARKING = 4,
  CROSSING_AID = 5,
  SPEED_BUMP = 6,
  POT_HOLE = 7,
  REFLECTOR = 8,
  STUD = 9,
  BOLLARD = 10,
  CRASH_ABSORBER = 11,
  BITUMEN = 12,
  MANHOLE_COVER = 13,
  GRATING = 14,
  RUT = 15,
  PUDDLE = 16,
  MISC = 17
};

enum class VVMRoadUserSubTypeBICYCLE {
  REGULAR = 0,
  EMERGENCY = 1,
  CONSTRUCTION = 2,
  WITH_RIDER = 3,
  WITHOUT_RIDER = 4
};

enum class VVMRoadUserSubTypeBUS {
  REGULAR = 0,
  EMERGENCY = 1,
  CONSTRUCTION = 2,
  TROLLEY_BUS = 3,
  BENDY_BUS = 4
};

enum class VVMRoadUserSubTypeGeneral {
  REGULAR = 0,
  EMERGENCY = 1,
  CONSTRUCTION = 2
};

enum class VVMRoadUserSubTypeMOTORCYCLE {
  REGULAR = 0,
  EMERGENCY = 1,
  CONSTRUCTION = 2,
  WITH_RIDER = 3,
  WITHOUT_RIDER = 4
};

enum class VVMRoadUserSubTypePEDESTRIAN {
  REGULAR = 0,
  EMERGENCY = 1,
  CONSTRUCTION = 2,
  CHILD = 3,
  ADULT = 4
};

enum class VVMRoadUserSubTypePERSONAL_MOBILITY_DEVICE {
  REGULAR = 0,
  EMERGENCY = 1,
  CONSTRUCTION = 2,
  WITH_RIDER = 3,
  WITHOUT_RIDER = 4
};

enum class VVMRoadUserSubTypeTRAILER {
  REGULAR = 0,
  EMERGENCY = 1,
  CONSTRUCTION = 2,
  CAR_TRAILER = 3,
  CARAVAN = 4,
  TRUCK_TRAILER = 5,
  TRAIN_TRAILER = 6,
  BENDY_BUS_TRAILER = 7
};

enum class VVMRoadUserSubTypeTRUCK {
  REGULAR = 0,
  EMERGENCY = 1,
  CONSTRUCTION = 2,
  STREET_CLEANING = 3
};

enum class VVMRoadUserSubTypeWHEELCHAIR {
  REGULAR = 0,
  EMERGENCY = 1,
  CONSTRUCTION = 2,
  WITH_RIDER = 3,
  WITHOUT_RIDER = 4
};

enum class VVMRoadUserType {
  REGULAR = 0,
  CAR = 1,
  TRUCK = 2,
  BUS = 3,
  MOTORCYCLE = 4,
  BICYCLE = 5,
  PEDESTRIAN = 6,
  PUSHABLE_PULLABLE = 7,
  WHEELCHAIR = 8,
  PERSONAL_MOBILITY_DEVICE = 9,
  TRAILER = 10,
  FARMING = 11,
  RAIL = 12,
  CARRIAGE = 13
};

enum class VVMRoadUserVehicleLights {
  UNKNOWN = -1,
  OFF = 0,
  ON = 1
};

enum class VVMSignSizeClass {
  UNKNOWN = 0,
  SMALL = 1,
  MIDDLE = 2,
  LARGE = 3
};

class VVMSignType {
public:
  const char* UNKNOWN = "0";
  const char* GIVE_WAY = "205";
  const char* STOP_GIVE_WAY = "206";
  const char* NO_PARKING = "283";
  const char* NO_PARKING_START = "283-10";
  const char* RESTRICTED_PARKING = "286";
  const char* PRIORITY = "301";
  const char* PARKING = "314";
  const char* DEAD_END = "357";
  const char* DEAD_END_CYCLISTS_AND_PEDESTRIANS_CAN_PASS = "357-50";
  const char* DEAD_END_PEDESTRIANS_CAN_PASS = "357-51";
  const char* TL_REGULAR = "2000-1";
  const char* TL_ARROW_STRAIGHT = "2000-2";
  const char* TL_ARROW_RIGHT = "2000-3";
  const char* TL_ARROW_LEFT = "2000-4";
  const char* TL_ARROW_STRAIGHT_RIGHT = "2000-5";
  const char* TL_ARROW_STRAIGHT_LEFT = "2000-6";
  const char* TL_PEDESTRIAN = "2000-7";
  const char* TL_BICYCLE = "2000-8";
  const char* TL_PEDESTRIAN_BICYCLE = "2000-9";
  const char* LIGHT_SINGLE = "2000-10";
  const char* TL_RED_AMBER = "2000-11";
  const char* LANE_LIGHT = "2000-12";
  const char* BUS_LIGHT = "2000-13";
  const char* SWITCHABLE = "3000-1";
  const char* BARRIER = "4000-1";
  const char* WALKWAY = "239";
  const char* CROSSING = "102";
  const char* BICYCLE_STREET_END = "244_2";
  const char* ZONE_30_START = "274_1";
  const char* NO_CYCLING = "254";
  const char* PARKING_WITH_TICKET = "1053-31";
  const char* PARKING_RESTRICTED_ZONE_START = "290_1";
  const char* PARKING_RESTRICTED_ZONE_END = "290_2";
  const char* END_OF_ABSOLUT_PARKING_RESTRICTION_END_RIGHT = "283-20";
  const char* BEGIN_OF_ABSOLUT_PARKING_RESTRICTION_END_RIGHT = "283-30";
  const char* PARKING_ON_SIDEWALK_HALF_RIGHT_CENTER = "315-58";
  const char* PARKING_ON_SIDEWALK_HALF_RIGHT_START = "315-56";
  const char* PEDESTRIAN_CROSSING_RIGHT = "350-10";
  const char* PEDESTRIAN_CROSSING_LEFT = "350-20";
  const char* PRIORITY_ROAD = "306";
  const char* NO_VEHICLES_ALLOWED = "250";
  const char* NO_ENTRY = "267";
  const char* CROSSING_BICYCLE_LEFT_RIGHT = "1000-32";
  const char* TRAFFIC_CALM_AREA_START = "325_1";
  const char* TRAFFIC_CALM_AREA_END = "325_2";
  const char* GUIDE_PLATE = "626-30";
  const char* PRESCRIBED_PASSING_RIGHT = "222";
  const char* PRESCRIBED_PASSING_LEFT = "222-10";
  const char* PRESCRIBED_DIRECTION_STRAIGHT_RIGHT = "214";
  const char* RESIDENTS_FREE = "1020-30";
  const char* MOTORWAY_RIGHT = "430-20";
  const char* CYCLISTS_ARE_ALLOWED = "1022-10";
  const char* MANDATORY_TURN_RIGHT = "209";
  const char* MANDATORY_TURN_LEFT = "209-10";
  const char* MANDATORY_STRAIGHT = "209-30";
  const char* BUS_STOP = "224";
  const char* MAXIMUM_SPEED_50 = "274-50";
};

enum class VVMStateValue {
  UNKNOWN = 0,
  GREEN = 1,
  AMBER = 2,
  RED = 3,
  RED_AMBER = 4,
  FLASHING_AMBER = 5,
  FLASHING_RED = 6,
  GREEN_ARROW = 7,
  RED_CROSS = 8,
  AMBER_DIAGONAL_ARROW_RIGHT = 9,
  AMBER_DIAGONAL_ARROW_LEFT = 10,
  ACTIVE = 11,
  INACTIVE = 12,
  BUS_STOP = 13,
  BUS_STRAIGHT = 14,
  BUS_RIGHT = 15,
  BUS_LEFT = 16,
  BUS_STOP_EXPECTED = 17,
  BUS_YIELD = 18,
  BUS_WILL_SWITCH = 19
};

enum class VVMStructuralObjectType {
  NOT_DECLARED = 0,
  VEGETATION = 1,
  BUILDING = 2,
  BUS_SHELTER = 3,
  TUNNEL = 4,
  BRIDGE = 5,
  FENCE = 6,
  BENCH = 7,
  ROAD_WORK = 8,
  BODY_OF_WATER = 9,
  GARAGE = 10,
  BILLBOARD = 11,
  ADVERTISING_PILLAR = 12,
  PHONE_BOX = 13,
  POST_BOX = 14,
  OVERHEAD_STRUCTURE = 15
};

enum class VVMSurfaceColor {
  UNKNOWN = 0,
  WHITE = 1,
  GREEN = 3,
  RED = 4,
  ANTHRACITE = 6,
  BROWN = 7
};

enum class VVMSurfaceCondition {
  NO_VALUE = 0,
  FINE = 1,
  CRACKS = 2,
  BITUMEN = 3,
  POT_HOLES = 4,
  RUTS = 5,
  DAMAGED = 6
};

enum class VVMSurfaceMaterial {
  UNKNOWN = 0,
  ASPHALT = 1,
  CONCRETE = 2,
  BRICK = 3,
  GRAVEL = 4
};

enum class VVMWeatherSource {
  UNKNOWN = 0,
  DWD = 1,
  EXTERNAL_SENSOR = 2
};

enum class VVMWind {
  CALM = 0,
  LIGHT_AIR = 1,
  LIGHT_BREEZE = 2,
  GENTLE_BREEZE = 3,
  MODERATE_BREEZE = 4,
  FRESH_BREEZE = 5,
  STRONG_BREEZE = 6,
  NEAR_GALE = 7,
  GALE = 8,
  STRONG_GALE = 9,
  STORM = 10,
  VIOLENT_STORM = 11,
  HURRICANE = 12
};
