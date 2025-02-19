import math
import numpy as np
from omega_format import StructuralObject, Polyline, ReferenceTypes
from .polyline import check_polyline
from ..logger import logger

def convert_objects_bridge(my_road, center_line_points, bridge, road):
    structural_obj_type = ReferenceTypes.StructuralObjectType.BRIDGE

    if road.lanes.lane_section is not None:
        lane_section = road.lanes.lane_section[0]
    else:
        logger.warning("No related lane sections for bridge-object were found. Object dropped.")
        return my_road

    polyline = get_polyline_for_bridge_tunnel(bridge.s, bridge.length, center_line_points, lane_section)

    if polyline:
        check_polyline(polyline, None)
        new_structural_object = StructuralObject(type=structural_obj_type, polyline=polyline)
        my_road.structural_objects.update({len(my_road.structural_objects): new_structural_object})
        # Lane.subtype is already identified in "extract_road_data"

    return my_road


def convert_objects_tunnel(my_road, center_line_points, tunnel, road):
    structural_obj_type = ReferenceTypes.StructuralObjectType.TUNNEL

    if road.lanes.lane_section is not None:
        lane_section = road.lanes.lane_section[0]
    else:
        logger.warning("No related lane sections for tunnel-object were found. Object dropped.")
        return my_road

    polyline = get_polyline_for_bridge_tunnel(tunnel.s[0], tunnel.length[0], center_line_points, lane_section)

    if polyline:
        check_polyline(polyline)
        new_structural_object = StructuralObject(type = structural_obj_type, polyline = polyline)
        my_road.structural_objects.update({len(my_road.structural_objects): new_structural_object})
        # Lane.subtype is already identified in "extract_road_data"
    return my_road


def get_polyline_for_bridge_tunnel(starting_point, length, center_line_points, lane_section):
    """
    Creates a polyline from a bridge or tunnel with the input of the starting s-coordinate ,length and width.
    :param starting_point:
    :param length: Legnth of tunnel/bridge along s-direction
    :param center_line_points:
    :param lane_section:
    :return:
    """
    # To archieve a continuous polyline a forward and backwards directed list of the coordinates is created which are appended later.
    pos_x_fw = []
    pos_y_fw = []
    pos_z_fw = []
    pos_x_bw = []
    pos_y_bw = []
    pos_z_bw = []
    start_index = 0

    for s in range(0, len(center_line_points) - 1):
        if s < len(center_line_points) - 1:
            if center_line_points[s, 0] < starting_point <= center_line_points[s+1, 0]:
                start_index = s
        else:
            if starting_point >= center_line_points[s, 0]:
                start_index = s

    width = get_road_width_from_lane_section(lane_section, center_line_points[start_index, 0])

    for s in range(start_index, len(center_line_points) - 1):
        if starting_point <= center_line_points[s, 0] < (starting_point + length):
            # width = get_road_width_from_lane_section(lane_section, center_line_points[s, 0])
            pos_x_fw.append(center_line_points[s, 1] - width * math.sin(center_line_points[s, 3]))
            pos_x_bw.append(center_line_points[s, 1] + width * math.sin(center_line_points[s, 3]))
            pos_y_fw.append(center_line_points[s, 2] + width * math.cos(center_line_points[s, 3]))
            pos_y_bw.append(center_line_points[s, 2] - width * math.cos(center_line_points[s, 3]))
            pos_z_fw.append(center_line_points[s, 4])
            pos_z_bw.append(center_line_points[s, 4])

    if pos_x_fw:
        pos_x = np.array(pos_x_fw + list(reversed(pos_x_bw)))
        pos_y = np.array(pos_y_fw + list(reversed(pos_y_bw)))
        pos_z = np.array(pos_z_fw + list(reversed(pos_z_bw)))

        return Polyline(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)
    else:
        logger.warning('Could not find matching s-value in center_line_points for bridge/tunnel object. No polyline'
              'could be created. Object is dropped.')
        return None


def get_road_width_from_lane_section(lane_section, current_s):
    """
    Bridge elements in openDrive do not inherit a width. Through the lane width element an assumption is made. Because
    the bridges s-value and the lane.width element are not related the width s_offset will be used for calculations in
    order to avoid abnormal width values. If the calculated value still is abnormal we assume a lane width of X meters
    per lane and multiply it by the number of lanes present.
    :param lane_section:
    :param current_s:
    :return:
    """
    lane_width_objects = []
    lane_width_values = []

    if lane_section.left_lanes:
        lane_width_objects = find_matching_width(lane_section.left_lanes, current_s)
    if lane_section.right_lanes:
        lane_width_objects = lane_width_objects + find_matching_width(lane_section.right_lanes, current_s)

    for width in lane_width_objects:
        current_lane_width_value = width.a + width.b * width.s_offset + width.c * pow(width.s_offset, 2) \
                                   + width.d * pow(width.s_offset, 3)
        lane_width_values.append(current_lane_width_value)

    width_total = sum(lane_width_values)
    if width_total < 0 or width_total > 25:
        nr_lanes = len(lane_section.left_lanes) + len(lane_section.right_lanes)
        width_per_lane = 3.0
        width_total = nr_lanes * width_per_lane

    return width_total


def find_matching_width(side_of_lanes, current_s):
    """
    Finds the matching width element for one side of the lane section (right or left lanes) for the given s-value.
    :param side_of_lanes:
    :param current_s:
    :return:
    """
    width_list = []
    for lane in side_of_lanes:
        if lane.width:
            for i in range(0, len(lane.width)):
                # if not last width element
                if i + 1 < len(lane.width):
                    # check if current_s is higher than next elements s_offset
                    if current_s > lane.width[i + 1].s_offset:
                        continue
                    else:
                        width_list.append(lane.width[i])
                        break
                else:
                    width_list.append(lane.width[i])

    return width_list
