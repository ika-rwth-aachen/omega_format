import copy
from omega_format import Boundary, ReferenceTypes
from .mapping import boundary_type_mapping, boundary_color_mapping, boundary_subtype_mapping
from ..logger import logger

def calculate_boundaries(lane_section, center_line_points, my_road, lookup_table, vvm_road_id):

    # check: center lane must always be present and should not contain any width
    if len(lane_section.center_lanes) == 0:
        logger.error("OpenDRIVE roads need to contain one center lane")
    elif len(lane_section.center_lanes) > 1:
        logger.error("OpenDRIVE roads are only allowed to have one single center lane")
    elif len(lane_section.center_lanes[0].width) != 0:
        logger.error("OpenDRIVE center lanes should not contain any width. It will be ignored")

    # get boundaries for vvm_road_id lanes, further boundaries might be added through object conversion
    # this only works for markings, curb, gras and dots
    # in omega format one lane can have multiple right and left boundaries (e.g. solid lane and guardrail)
    # go over all lanes of current road and find corresponding openDRIVE lanes in lane_section via lookup_table
    for i in range(0, len(my_road.lanes)):
        # find this lane of road vvm_road_id in lookup table
        for j in range(0, len(lookup_table)):
            if lookup_table[j][3] == vvm_road_id:
                # search for lane vvm number
                for k in range(j, len(lookup_table)):
                    if lookup_table[j][4] == i:
                        # get openDRIVE lane id
                        opendrive_lane_id = lookup_table[j][2]
                        break
                break

        # set up data structure for left boundary (right lane of previous lane)
        left_boundary_next = []
        # go through left and right lanes
        sides = dict(
            left=lane_section.left_lanes,
            right=lane_section.right_lanes,
        )
        for side_flag, lanes_of_side in sides.items():
            # find lane with opendrive_lane_id in lane_section
            for j in range(0, len(lanes_of_side)):
                if lanes_of_side[j].id == opendrive_lane_id:
                    # get boundaries (markings are right boundaries of current lane and
                    # left boundary is that of previous lane)
                    # if first lane --> left boundary = center lane
                    if abs(opendrive_lane_id) == 1:
                        # set up data structure for left boundary (right lane of previous lane)
                        left_boundary_next = []
                        # center lane
                        for k in range(0, len(lane_section.center_lanes[0].road_mark)):
                            # if not last entry
                            if k != len(lane_section.center_lanes[0].road_mark)-1:
                                my_boundary = set_boundary(center_line_points,
                                                           lane_section.center_lanes[0].road_mark[k].s_offset,
                                                           lane_section.center_lanes[0].road_mark[k+1].s_offset,
                                                           False, False, lane_section.center_lanes[0].road_mark[k])
                            # last entry (not road_mark s_offset of last entry is given to function
                            # (as it does not exist), but last point in center_line_points
                            else:
                                my_boundary = set_boundary(center_line_points,
                                                           lane_section.center_lanes[0].road_mark[k].s_offset,
                                                           len(center_line_points) - 1, True, False,
                                                           lane_section.center_lanes[0].road_mark[k])

                            left_boundary_next.append(my_boundary)

                    # else left boundary right boundary of previous lane
                    # left boundary equals right boundary of previous lane
                    for k in range(0, len(left_boundary_next)):
                        my_road.lanes[i].boundaries.update({len(my_road.lanes[i].boundaries): left_boundary_next[k]})

                    # reset
                    left_boundary_next = []

                    # get right boundary
                    for k in range(0, len(lanes_of_side[j].road_mark)):
                        # if not last entry
                        if k != len(lanes_of_side[j].road_mark) - 1:
                            my_boundary = set_boundary(center_line_points,
                                                       lanes_of_side[j].road_mark[k].s_offset,
                                                       lanes_of_side[j].road_mark[k + 1].s_offset, False,
                                                       True, lanes_of_side[j].road_mark[k])
                        # if last entry
                        else:
                            my_boundary = set_boundary(center_line_points,
                                                       lanes_of_side[j].road_mark[k].s_offset,
                                                       len(center_line_points) - 1, True, True,
                                                       lanes_of_side[j].road_mark[k])
                        my_road.lanes[i].boundaries.update({len(my_road.lanes[i].boundaries): my_boundary})
                        # set for left boundary of neighboring lane
                        # (copy by value otherwise entry in my_roads will be changed)
                        my_boundary_aux = copy.deepcopy(my_boundary)
                        my_boundary_aux.is_right_boundary = False
                        left_boundary_next.append(my_boundary_aux)
                    break

        # check if boundaries exist for both sides
        my_road = check_lanes_boundary(my_road, center_line_points, i)

    return my_road


def set_boundary(center_line_points, current_road_mark_s, next_road_mark_s, last, right, current_road_mark):

    my_boundary = Boundary()
    # get start index
    for l in range(0, len(center_line_points) - 1):
        if center_line_points[l, 0] <= current_road_mark_s < center_line_points[l + 1, 0]:
            my_boundary.poly_index_start = l
            break
    # get end index
    if last:
        my_boundary.poly_index_end = next_road_mark_s
    else:
        for l in range(0, len(center_line_points) - 1):
            # end point = start point of next road mark
            if center_line_points[l, 0] <= next_road_mark_s < center_line_points[l + 1, 0]:
                my_boundary.poly_index_end = l
                break
    if right:
        my_boundary.is_right_boundary = True
    else:
        my_boundary.is_right_boundary = False

    # type, material, color Mapping
    my_boundary.type = 0x0
    my_boundary.condition = 0x0
    my_boundary.height = 0x0
    my_boundary.subtype = 0x0
    my_boundary.color = 0x0

    if current_road_mark is not None:

        if current_road_mark.type is not None:
            my_boundary.type = boundary_type_mapping(current_road_mark.type)

            # double check if solid or dashed line is on the right side through lane_change attribute, only
            if my_boundary.type == ReferenceTypes.BoundaryType.SOLID_DASHED:
                if current_road_mark.lane_change:
                    if current_road_mark.lane_change == "increase":
                        my_boundary.type = ReferenceTypes.BoundaryType.DASHED_SOLID

            elif my_boundary.type == ReferenceTypes.BoundaryType.DASHED_SOLID:
                if current_road_mark.lane_change:
                    if current_road_mark.lane_change == "decrease":
                        my_boundary.type = ReferenceTypes.BoundaryType.SOLID_DASHED

        if current_road_mark.color is not None:
            my_boundary.color = boundary_color_mapping(current_road_mark.color)

        if current_road_mark.material is not None:
            my_boundary.subtype = boundary_subtype_mapping(current_road_mark.material)

    return my_boundary


def check_lanes_boundary(my_road, center_line_points, i):

    # if no boundary is present input two generic ones
    if not my_road.lanes[i].boundaries:
        my_road = set_placeholder_boundary(my_road, center_line_points, i, False)
        my_road = set_placeholder_boundary(my_road, center_line_points, i, True)

    # when at least one boundary is present check if there is a right AND a left one, otherwise add the missing side
    else:
        right_boundary_exists = False
        left_boundary_exists = False
        # iterate through and check for present sides
        for boundary in my_road.lanes[i].boundaries.values():
            if boundary.is_right_boundary:
                right_boundary_exists = True
            else:
                left_boundary_exists = True
        # update right side
        if not right_boundary_exists:
            my_road = set_placeholder_boundary(my_road, center_line_points, i, True)
        # update left side
        if not left_boundary_exists:
            my_road = set_placeholder_boundary(my_road, center_line_points, i, False)

    return my_road


def set_placeholder_boundary(my_road, center_line_points, i, is_right):
    my_boundary = set_boundary(center_line_points, 0, len(center_line_points) - 1, True, is_right, None)
    my_road.lanes[i].boundaries.update({len(my_road.lanes[i].boundaries): my_boundary})
    return my_road
