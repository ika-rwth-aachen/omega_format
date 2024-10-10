from omega_format import ReferenceTypes
from ..logger import logger
'''
Sources:
- Type Definitions of OpenDRIVE by researched by Stefan: DERIVED FROM: https://opendrive-uml.web.app/.
- Signal list of VVM Format
- Documentation of OpenDRIVE: https://www.asam.net/index.php?eID=dumpFile&t=f&f=4089&token=deea5d707e2d0edeeb4fccd544a973de4bc46a09#_foreword
'''


def road_location_mapping(value: str):
    # can be gathered from type (see converter.py set_location, take only first type if multiple are available)
    road_location = {
        "unknown": ReferenceTypes.RoadLocation.UNKNOWN,
        "rural": ReferenceTypes.RoadLocation.NON_URBAN,
        "motorway": ReferenceTypes.RoadLocation.HIGHWAY,
        "town": ReferenceTypes.RoadLocation.URBAN,
        "lowspeed": ReferenceTypes.RoadLocation.URBAN,
        "pedestrian": ReferenceTypes.RoadLocation.UNKNOWN,     # unclear
        "bicycle": ReferenceTypes.RoadLocation.UNKNOWN,    # unclear
        "townexpressway": ReferenceTypes.RoadLocation.URBAN,
        "townarterial": ReferenceTypes.RoadLocation.URBAN,
        "townprivate": ReferenceTypes.RoadLocation.URBAN,
        "townlocal": ReferenceTypes.RoadLocation.URBAN,
        "townplaystreet": ReferenceTypes.RoadLocation.URBAN,
        "test": ReferenceTypes.RoadLocation.UNKNOWN,
    }
    return road_location[value]


def lane_type_mapping(value: str):
    lane_types = {
        "driving": ReferenceTypes.LaneType.DRIVING,
        "stop": ReferenceTypes.LaneType.SHOULDER,
        "none": ReferenceTypes.LaneType.FREESPACE, # probably not the same
        "restricted": ReferenceTypes.LaneType.KEEPOUT,
        "median": ReferenceTypes.LaneType.VEGETATION,
        "biking": ReferenceTypes.LaneType.BICYCLE_LANE,
        "sidewalk": ReferenceTypes.LaneType.WALKWAY,
        "shoulder": ReferenceTypes.LaneType.FREESPACE,
        "exit": ReferenceTypes.LaneType.OFF_RAMP,
        "entry": ReferenceTypes.LaneType.ON_RAMP,
        "onramp": ReferenceTypes.LaneType.ON_RAMP,
        "offramp": ReferenceTypes.LaneType.OFF_RAMP,
        "connectingramp": ReferenceTypes.LaneType.ON_RAMP,
        "bidirectional": ReferenceTypes.LaneType.DRIVING,
        "tram": ReferenceTypes.LaneType.RAIL,
        "rail": ReferenceTypes.LaneType.RAIL,
        "bus": ReferenceTypes.LaneType.BUS_LANE,
        "taxi": ReferenceTypes.LaneType.BUS_LANE, # bus_bicycle?
        "hov": ReferenceTypes.LaneType.CARPOOL_LANE,
        "mwyentry": ReferenceTypes.LaneType.ON_RAMP,
        "mwyexit": ReferenceTypes.LaneType.OFF_RAMP,
        "special1": ReferenceTypes.LaneType.UNKNOWN,
        "special2": ReferenceTypes.LaneType.UNKNOWN,
        "special3": ReferenceTypes.LaneType.UNKNOWN,
    }
    if value.lower() in lane_types.keys():
        return lane_types.get(value.lower())


def lane_type_to_lane_width_mapping(value: str):
    lane_types = {
        "driving": ReferenceTypes.LaneType.DRIVING,
        "exit": ReferenceTypes.LaneType.OFF_RAMP,
        "entry": ReferenceTypes.LaneType.ON_RAMP,
        "onramp": ReferenceTypes.LaneType.ON_RAMP,
        "offramp": ReferenceTypes.LaneType.OFF_RAMP,
        "connectingramp": ReferenceTypes.LaneType.ON_RAMP,
        "bidirectional": ReferenceTypes.LaneType.DRIVING,
        "tram": ReferenceTypes.LaneType.RAIL,
        "rail": ReferenceTypes.LaneType.RAIL,
        "bus": ReferenceTypes.LaneType.BUS_LANE,
        "taxi": ReferenceTypes.LaneType.BUS_LANE, # bus_bicycle?
        "hov": ReferenceTypes.LaneType.CARPOOL_LANE,
        "mwyentry": ReferenceTypes.LaneType.ON_RAMP,
        "mwyexit": ReferenceTypes.LaneType.OFF_RAMP,
        "special1": ReferenceTypes.LaneType.UNKNOWN,
        "special2": ReferenceTypes.LaneType.UNKNOWN,
        "special3": ReferenceTypes.LaneType.UNKNOWN,
    }
    if value.lower() in lane_types.keys():
        return True


def lane_type_to_object_mapping(value: str):
    object_lane_types = {
        "roadworks": ReferenceTypes.StructuralObjectType.ROAD_WORK,
        "parking": ReferenceTypes.RoadObjectType.PARKING,
    }
    if value.lower() in object_lane_types.keys():
        return object_lane_types.get(value.lower())


def lane_type_to_boundary_mapping(value: str):
    boundary_lane_types = {
        "curb": ReferenceTypes.BoundaryType.CURB,
        "border": ReferenceTypes.BoundaryType.CURB,  # border in opendrive has same height as the road, hard material
    }
    if value.lower() in boundary_lane_types.keys():
        return boundary_lane_types.get(value.lower())


def boundary_type_mapping(value: str):
    # only markings can be retrieved from road mark per lane.
    # Other boundaries need to be retrieved via road objects in OpenDRIVE
    road_mark_to_boundary_types = {
        "none": ReferenceTypes.BoundaryType.UNKNOWN,
        "solid": ReferenceTypes.BoundaryType.SOLID,
        "broken": ReferenceTypes.BoundaryType.DASHED,
        "solid solid": ReferenceTypes.BoundaryType.SOLID_SOLID,
        "solid broken": ReferenceTypes.BoundaryType.SOLID_DASHED,
        "broken solid": ReferenceTypes.BoundaryType.DASHED_SOLID,
        "broken broken": ReferenceTypes.BoundaryType.DASHED_CHANGE_DIRECTION_LANE,
        "botts dots": ReferenceTypes.BoundaryType.STUDS,
        "grass": ReferenceTypes.BoundaryType.MISC,      # TODO not the perfect match but vvm does not have vegetation as boundary
        "curb": ReferenceTypes.BoundaryType.CURB,
        "border": ReferenceTypes.BoundaryType.CURB,     # border in opendrive has the same height as the road
        "custom": ReferenceTypes.BoundaryType.MISC,     # TODO custom road marks should have a detailed description in child tag
        "edge": ReferenceTypes.BoundaryType.UNKNOWN,   # TODO "edge: describing the limit of usable space on a road" ?
    }
    if value.lower() in road_mark_to_boundary_types.keys():
        return road_mark_to_boundary_types.get(value.lower())


def boundary_subtype_mapping(value: str):
    # opendrive road_mark material matches vvm subtype partly
    boundary_subtype = {
        "standard": ReferenceTypes.BoundarySubType.UNKNOWN,    # opendrive default value
        "thin": ReferenceTypes.BoundarySubType.THIN,
        "thick": ReferenceTypes.BoundarySubType.THICK,
        "metal": ReferenceTypes.BoundarySubType.METAL,
        "wood": ReferenceTypes.BoundarySubType.WOODEN,
        "wooden": ReferenceTypes.BoundarySubType.WOODEN,
    }
    if value.lower() in boundary_subtype.keys():
        return boundary_subtype.get(value.lower())
    else:
        logger.info("Boundary Subtype unknown, this might be because identifiers in OpenDrive are user defined "
              "- add new ones to mapping if neccessary! Unknown Value: " + value)


def boundary_color_mapping(value: str):
    # color can be found in road mark per lane
    boundary_color = {
        "standard": ReferenceTypes.BoundaryColor.WHITE,
        "blue": ReferenceTypes.BoundaryColor.UNKNOWN, # blue is not part of vvm
        "green": ReferenceTypes.BoundaryColor.GREEN,
        "red": ReferenceTypes.BoundaryColor.RED,
        "white": ReferenceTypes.BoundaryColor.WHITE,
        "yellow": ReferenceTypes.BoundaryColor.YELLOW,
        "orange": ReferenceTypes.BoundaryColor.UNKNOWN, # probably yellow as well?
    }
    if value.lower() in boundary_color.keys():
        return boundary_color.get(value.lower())
    else:
        logger.info("Boundary Color unknown. Unknown value: " + value)


def lateral_marking_color_mapping(value: str):
    # color can be found in road mark per lane
    lateral_marking_color = {
        "standard": ReferenceTypes.LateralMarkingColor.WHITE,
        "blue": ReferenceTypes.LateralMarkingColor.UNKNOWN, # blue is not part of vvm
        "green": ReferenceTypes.LateralMarkingColor.GREEN,
        "red": ReferenceTypes.LateralMarkingColor.RED,
        "white": ReferenceTypes.LateralMarkingColor.WHITE,
        "yellow": ReferenceTypes.LateralMarkingColor.YELLOW,
        "orange": ReferenceTypes.LateralMarkingColor.UNKNOWN, # probably yellow as well?
        "violet": ReferenceTypes.LateralMarkingColor.UNKNOWN
    }
    if value.lower() in lateral_marking_color.keys():
        return lateral_marking_color.get(value.lower())
    else:
        logger.info("Lateral marking color unknown. Unknown value: " + value)


def object_type_mapping(value: str):
    # car, van, bus, trailer, bike, motorbike, tram, train, pedestrian, wind are all deprecated
    object_type = {
        "none": ReferenceTypes.RoadObjectType.UNKNOWN,
        "obstacle": ReferenceTypes.RoadObjectType.MISC,
        "pole": ReferenceTypes.RoadObjectType.BOLLARD,
        "guidepost": ReferenceTypes.RoadObjectType.BOLLARD,
        "barrier": ReferenceTypes.RoadObjectType.CRASH_ABSORBER,
        "parkingspace": ReferenceTypes.RoadObjectType.PARKING,
        "patch": ReferenceTypes.RoadObjectType.BITUMEN,
        "trafficisland": ReferenceTypes.RoadObjectType.TRAFFIC_ISLAND,
        "streetlamp": ReferenceTypes.RoadObjectType.STREET_LAMP,
    }
    if value.lower() in object_type.keys():
        return object_type.get(value.lower())


def object_drivable_mapping(value):
    object_drivable = {
        ReferenceTypes.RoadObjectType.UNKNOWN: False,
        ReferenceTypes.RoadObjectType.MISC: False,
        ReferenceTypes.RoadObjectType.BOLLARD: False,
        ReferenceTypes.RoadObjectType.CRASH_ABSORBER: False,
        ReferenceTypes.RoadObjectType.PARKING: True,
        ReferenceTypes.RoadObjectType.BITUMEN: True,
        ReferenceTypes.RoadObjectType.TRAFFIC_ISLAND: False, # some might be?
        ReferenceTypes.RoadObjectType.STREET_LAMP: False,
    }
    if value in object_drivable.keys():
        return object_drivable.get(value)


def object_walkable_mapping(value):
    object_walkable = {
        ReferenceTypes.RoadObjectType.UNKNOWN: False,
        ReferenceTypes.RoadObjectType.MISC: False,
        ReferenceTypes.RoadObjectType.BOLLARD: False,
        ReferenceTypes.RoadObjectType.CRASH_ABSORBER: False,
        ReferenceTypes.RoadObjectType.PARKING: True,
        ReferenceTypes.RoadObjectType.BITUMEN: True,
        ReferenceTypes.RoadObjectType.TRAFFIC_ISLAND: False, # some might be?
        ReferenceTypes.RoadObjectType.STREET_LAMP: False,
    }
    if value in object_walkable.keys():
        return object_walkable.get(value)


def object_to_structural_object_mapping(value: str):
    object_structural = {
        "tree": ReferenceTypes.StructuralObjectType.VEGETATION,
        "vegetation": ReferenceTypes.StructuralObjectType.VEGETATION,
        "building": ReferenceTypes.StructuralObjectType.BUILDING,
        "gantry": ReferenceTypes.StructuralObjectType.OVERHEAD_STRUCTURE, # not sure
    }
    if value.lower() in object_structural.keys():
        return object_structural.get(value.lower())


def object_to_boundary_mapping(value: str):
    object_boundary = {
        "railing": ReferenceTypes.BoundaryType.GUARD_RAIL,
        "soundbarrier": ReferenceTypes.BoundaryType.NOISE_PROTECTION_WALL,
        "barrier": ReferenceTypes.BoundaryType.DIVIDER,
    }
    if value.lower() in object_boundary.keys():
        return object_boundary.get(value.lower())


def object_to_marking_mapping(value: str):
    object_marking = {
        "crosswalk": ReferenceTypes.LateralMarkingType.CROSSWALK,
        "zebracrossing": ReferenceTypes.LateralMarkingType.CROSSWALK,
        "roadmark": ReferenceTypes.LateralMarkingType.UNKNOWN,
        "roadpainting": ReferenceTypes.LateralMarkingType.UNKNOWN,
    }
    if value.lower() in object_marking.keys():
        return object_marking.get(value.lower())


def signal_type_mapping(value: str):
    try:
        return ReferenceTypes.SignType(value)
    except TypeError:
        return None


def signal_to_flat_marking_mapping(value: str):
    # by now only used: https://de.wikipedia.org/wiki/Bildtafel_der_Verkehrszeichen_in_der_Bundesrepublik_Deutschland_seit_2017
    signal_to_flat_marking = {
        "297-1": ReferenceTypes.FlatMarkingType.UNKNOWN, #TODO what type was here
        "297-121": ReferenceTypes.FlatMarkingType.NOTICE_ARROW,
        "298-1": ReferenceTypes.FlatMarkingType.KEEPOUT_AREA,
        "299-1": ReferenceTypes.FlatMarkingType.ZIG_ZAG,
    }
    if value.lower() in signal_to_flat_marking.keys():
        return signal_to_flat_marking.get(value.lower())


def signal_to_lateral_marking_mapping(value: str):
    # by now only used: https://de.wikipedia.org/wiki/Bildtafel_der_Verkehrszeichen_in_der_Bundesrepublik_Deutschland_seit_2017
    signal_to_lateral_marking = {
        "293-1": ReferenceTypes.LateralMarkingType.CROSSWALK,
        "294-1": ReferenceTypes.LateralMarkingType.STOP_LINE,
    }
    if value.lower() in signal_to_lateral_marking.keys():
        return signal_to_lateral_marking.get(value.lower())


def signal_shape_mapping(value):
    shape_round = {
        ReferenceTypes.SignType.MANDATORY_TURN_RIGHT: 0,
        ReferenceTypes.SignType.MANDATORY_TURN_LEFT: 0,
        ReferenceTypes.SignType.MANDATORY_STRAIGHT: 0,
        ReferenceTypes.SignType.PRESCRIBED_DIRECTION_STRAIGHT_RIGHT: 0,
        ReferenceTypes.SignType.PRESCRIBED_PASSING_RIGHT: 0,
        ReferenceTypes.SignType.PRESCRIBED_PASSING_LEFT: 0,
        ReferenceTypes.SignType.WALKWAY: 0,
        ReferenceTypes.SignType.NO_VEHICLES_ALLOWED: 0,
        ReferenceTypes.SignType.NO_ENTRY: 0,
        ReferenceTypes.SignType.MAXIMUM_SPEED_50: 0,
        ReferenceTypes.SignType.NO_PARKING: 0,
        ReferenceTypes.SignType.NO_PARKING_START: 0,
        # TODO
        #ReferenceTypes.SignType.: 0, 
        #ReferenceTypes.SignType.BEGIN_OF_ABSOLUT_PARKING_RESTRICTION_END_RIGHT: 0,
        ReferenceTypes.SignType.RESTRICTED_PARKING: 0,
        ReferenceTypes.SignType.MOTORWAY_RIGHT: 0,
    }
    if value in shape_round.keys():
        return shape_round.get(value, 1)
    else:
        # value 1 is for non-round signals
        return 1


def signal_fallback_master_mapping(value):
    fallback_master = {
        ReferenceTypes.SignType.TL_REGULAR: True,
        ReferenceTypes.SignType.TL_BICYCLE: True,
        ReferenceTypes.SignType.TL_PEDESTRIAN: True,
        ReferenceTypes.SignType.TL_RED_AMBER: True,
        ReferenceTypes.SignType.TL_ARROW_LEFT: True,
        ReferenceTypes.SignType.TL_ARROW_RIGHT: True,
        ReferenceTypes.SignType.TL_ARROW_STRAIGHT: True,
        ReferenceTypes.SignType.TL_ARROW_STRAIGHT_LEFT: True,
        ReferenceTypes.SignType.TL_ARROW_STRAIGHT_RIGHT: True,
        ReferenceTypes.SignType.TL_PEDESTRIAN_BICYCLE: True,
        ReferenceTypes.SignType.LIGHT_SINGLE: True,
        ReferenceTypes.SignType.BUS_LIGHT: True,
        ReferenceTypes.SignType.SWITCHABLE: True,
    }
    if value in fallback_master.keys():
        return fallback_master.get(value)
    else:
        # if not in above dict, not qualified for fallback option
        return False


def signal_fallback_slave_mapping(value):
    fallback_slave = {
        ReferenceTypes.SignType.GIVE_WAY: True,
        ReferenceTypes.SignType.STOP_GIVE_WAY: True,
        ReferenceTypes.SignType.PRIORITY: True,
        ReferenceTypes.SignType.PRIORITY_ROAD: True,
        ReferenceTypes.SignType.CROSSING: True,
        ReferenceTypes.SignType.BARRIER: True,
    }
    if value in fallback_slave.keys():
        return fallback_slave.get(value)
    else:
        # if not in above dict, not qualified for fallback option
        return False
