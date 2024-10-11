from .mapping import *  # noqa: F403
from .boundary import calculate_boundaries
from .lane import calculate_borders, calculate_lanes, get_lane_subtype, get_lane_class, calculate_s_index
from .signals import get_road_signals
from .objects import get_road_objects
from .centerLinePoints import get_center_line_points
from omega_format import ReferenceTypes, Road
from ..logger import logger


def process_road(my_roads, road, my_opendrive, step_size, lookup_table, reference_table):
    my_road = Road()
    # set location to information in type (multiple types allowed in openDrive --> set to first one)
    my_road = set_location(my_road, road)


    # get centerline points, needs to be truncated later in case of multiple lane sections
    center_line_points, clp_no_offset, n_coordinates_per_segment = get_center_line_points(road, step_size)
    #indexes = np.cumsum(np.concatenate([[0],n_coordinates_per_segment]))
    # get end point in center_line_point for first lane section if multiple lane sections are present
    start_point_index = calculate_s_index(center_line_points, road.lanes.lane_section[0].s)
    if len(road.lanes.lane_section)>1:
        end_point_index =  calculate_s_index(center_line_points, road.lanes.lane_section[1].s)
    else:
        end_point_index = len(center_line_points)-1

    # first lane section: get all borders, lanes and further information (signs, markings, objects etc.)
    my_road, lookup_table, reference_table = extract_road_data(0, center_line_points, end_point_index,
                                                               start_point_index, my_road, road, lookup_table,
                                                               len(my_roads.roads_list), my_opendrive.junction_group,
                                                               reference_table, clp_no_offset, step_size)

    # add road to my_roads list of roads
    my_roads.roads_list.update({len(my_roads.roads_list): my_road})

    # if new lane section is found, new road needs to be created in vvm format
    # run border extraction etc. for other lane sections if present

    for i in range(1, len(road.lanes.lane_section)):
        start_point_index = calculate_s_index(center_line_points, road.lanes.lane_section[i].s)
        if i<len(road.lanes.lane_section)-1:
            end_point_index =  calculate_s_index(center_line_points, road.lanes.lane_section[i+1].s)
        else:
            end_point_index = len(center_line_points)-1

        my_roads, lookup_table, reference_table = create_road_per_lane_section(i, center_line_points,
                                                                                my_road.location,
                                                                                end_point_index, road,
                                                                                my_roads, start_point_index,
                                                                                lookup_table,
                                                                                my_opendrive.junction_group,
                                                                                reference_table,
                                                                                clp_no_offset, step_size)

      
    return my_roads, lookup_table, reference_table


def set_location(my_road, road):
    try:
        if road.type[0].type is not None:
            my_road.location = road_location_mapping(road.type[0].type)  # noqa: F405
        else:
            my_road.location = ReferenceTypes.RoadLocation.UNKNOWN
    except IndexError:
        # according to openDRIVE docu type can be zero --> set to
        # type seems not to be available for roads that are part of an intersection
        logger.info(f"Road should have a type, otherwise road location can not be determined. Road id: {road.id}")
        my_road.location = ReferenceTypes.RoadLocation.UNKNOWN

    if len(road.type) > 1:
        logger.warning(f"Road has more than one type. This is not yet supported, and only the first one is considered for now. Road id: {road.id}")

    return my_road


def create_road_per_lane_section(index, center_line_points, location, end_point_index, road, my_roads,
                                 start_point_index, lookup_table, junction_group, reference_table, clp_no_offset,
                                 step_size):

    # if openDRIVE file has multiple lane sections, each needs to be new road in vvm hdf5
    my_road = Road()
    my_road.location = location
    my_road, lookup_table, reference_table = extract_road_data(index, center_line_points, end_point_index,
                                                               start_point_index, my_road, road, lookup_table,
                                                               len(my_roads.roads_list), junction_group,
                                                               reference_table, clp_no_offset, step_size)

    # insert into my_roads structure
    my_roads.roads_list.update({len(my_roads.roads_list): my_road})

    return my_roads, lookup_table, reference_table


def extract_road_data(index, center_line_points, end_point_index, start_point_index, my_road, road, lookup_table,
                      vvm_road_id, junction_group, reference_table, clp_no_offset, step_size):
    """
    Extracts all data from the input road, including geometrical data as its borders polyline as well es every other
    informations stored within.
    :param step_size:
    :param clp_no_offset:
    :param index: lane_section_index
    :param center_line_points: table of center_line_points [s,x,y,hdg,z,superelevation]
    :param end_point_index: lane_sections end point index in center_line_points table
    :param start_point_index: lane_sections start point index in center_line_points table
    :param my_road: vvm_road
    :param road: opendrive_road
    :param lookup_table: [opendrive_road_id, opendrive_lanesection_id, opendrive_lane_id, vvm_road_id, vvm_lane_id]
    :param vvm_road_id:
    :param junction_group:
    :param reference_table:
    :return:
    """
    # get borders for index lane section
    my_road = calculate_borders(road.lanes.lane_section[index], center_line_points, end_point_index, start_point_index,
                                my_road, road, step_size)


    # get lane class (junction etc.)
    lane_class = get_lane_class(road.junction, junction_group)

    # get lane subtype (bridge, tunnel)
    lane_subtype = get_lane_subtype(road)

    # get actual lanes
    my_road, lookup_table = calculate_lanes(road.lanes.lane_section[index], my_road, road.id, index, lookup_table,
                                            vvm_road_id, lane_class, lane_subtype)

    # get boundary objects (marking, curb etc.)
    my_road = calculate_boundaries(road.lanes.lane_section[index], center_line_points, my_road, lookup_table,
                                   vvm_road_id)

    # get road objects
    my_road = get_road_objects(my_road, road, clp_no_offset, lookup_table, index, vvm_road_id, step_size)

    # get road signals
    my_road, reference_table = get_road_signals(my_road, road, clp_no_offset, lookup_table, reference_table,
                                                vvm_road_id)

    return my_road, lookup_table, reference_table



