from omega_format import RoadObject, StructuralObject, LateralMarking, Boundary, ReferenceTypes
from ..logger import logger
from .mapping import object_to_marking_mapping, object_type_mapping, object_to_structural_object_mapping,\
    object_drivable_mapping, object_walkable_mapping, object_to_boundary_mapping, lateral_marking_color_mapping
from .objectsTunnelBridge import convert_objects_bridge, convert_objects_tunnel
from .polyline import calculate_polyline, calculate_object_center_point, interpolate_linear, get_outlines_max_height,\
    get_polyline_from_width, get_polyline_from_point, create_polyline_from_list, sum_two_polylines,\
    get_polyline_for_rect_obj_repeat, check_polyline
import math


def get_road_objects(my_road, road, center_line_points, lookup_table, index, vvm_road_id, step_size):
    # center_line_points is a 6-dimensional list: [s, x, y, heading, z, superelevation]
    if road.objects is not None:

        # Bridge
        if road.objects.bridge is not None:
            for bridge in road.objects.bridge:
                my_road = convert_objects_bridge(my_road, center_line_points, bridge, road)

        # Tunnel
        if road.objects.tunnel is not None:
            for tunnel in road.objects.tunnel:
                my_road = convert_objects_tunnel(my_road, center_line_points, tunnel, road)

        # Objects (& Objects Repeat)
        if road.objects.object is not None:
            for odr_object in road.objects.object:
                my_road = process_object(my_road, center_line_points, odr_object, lookup_table, index, vvm_road_id,
                                         step_size)

        # Reference
        if road.objects.object_reference is not None:
            pass
            """
            -   In Opendrive objects are defined per road and have a validity for certain lanes. With the reference
                element this is transfered to other roads. A system we do not have. Objects are not of the same type
                and do not have regulatory purposes in omega_format. There are no cases where the referencing is
                necessary to convert in some sort of way.
            """

    return my_road


def convert_object(my_road, odr_object, center_line_points, lookup_table, vvm_road_id, index, polyline=None,
                   height=0.0):
    if not polyline:
        logger.warning(f'Object contains no polyline. Object is dropped. Object id is: {odr_object.id}')
        # if polyline is none the object was provided with neither radius nor width or length --> it can not be created
        return my_road

    else:
        # Object Type Mapping
        if object_type_mapping(odr_object.type) is not None:
            new_object = create_object(polyline, odr_object.type, height)
            my_road.road_objects.update({len(my_road.road_objects): new_object})
            return my_road
        """
        Some OpenDrive mapping tools dont seem to follow the official guidelines and use other name definitions instead.
        Here are additional tests to identify objects as parking spaces: via naming-scheme and mandatory attributes 
        """
        if odr_object.parking_space:
            new_object = create_object(polyline, "parkingSpace")
            my_road.road_objects.update({len(my_road.road_objects): new_object})
            return my_road

        if odr_object.type == "parking":
            new_object = create_object(polyline, "parkingSpace")
            my_road.road_objects.update({len(my_road.road_objects): new_object})
            return my_road

        # Object to Structural Objects
        if object_to_structural_object_mapping(odr_object.type) is not None:
            new_structural_object = create_structural_object(polyline, odr_object.type)
            my_road.structural_objects.update({len(my_road.structural_objects): new_structural_object})
            return my_road

        # Object to Boundary Mapping
        if object_to_boundary_mapping(odr_object.type) is not None:
            my_road = create_boundary_from_object(my_road, center_line_points, lookup_table, odr_object, index, vvm_road_id,
                                                  polyline)
            return my_road

        # Object to Lateral Marking Mapping
        if object_to_marking_mapping(odr_object.type) is not None:  # crosswalk is the only convertible type
            long_size = 0.0
            if odr_object.length:
                if odr_object.length is not None:
                    long_size = odr_object.length
            new_object = create_lateral_marking(polyline, odr_object, long_size)
            if new_object:
                my_road.lateral_markings.update({len(my_road.lateral_markings): new_object})
            return my_road

        # Unknown Type
        obj_type = ReferenceTypes.StructuralObjectType.NOT_DECLARED
        new_object = RoadObject(type=obj_type, polyline=polyline, walkable=False, drivable=False)
        new_object.height = height
        my_road.road_objects.update({len(my_road.road_objects): new_object})
        return my_road


def create_object(polyline, object_type, height=0.0):
    new_object = RoadObject(polyline=polyline, type=object_type_mapping(object_type))
    new_object.height = height
    new_object.drivable = object_drivable_mapping(new_object.type)
    new_object.walkable = object_walkable_mapping(new_object.type)
    return new_object


def convert_lane_to_object(my_road, left_index, right_index, object_type):
    polyline_left = my_road.borders[left_index].polyline
    polyline_right = my_road.borders[right_index].polyline
    # Border consists only of a polyline - both references have to be summed up into one polyline
    polyline_total = sum_two_polylines(polyline_left, polyline_right)
    # create object depending on its type
    if object_type == ReferenceTypes.StructuralObjectType.ROAD_WORK:
        new_structural_object = StructuralObject(polyline=polyline_total,
                                                 type=ReferenceTypes.StructuralObjectType.ROAD_WORK, height=0.0)
        my_road.structural_objects.update({len(my_road.structural_objects): new_structural_object})
    if object_type == ReferenceTypes.RoadObjectType.PARKING:
        new_object = RoadObject(polyline=polyline_total, type=ReferenceTypes.RoadObjectType.PARKING, height=0.0)
        new_object.drivable = True
        new_object.walkable = True
        my_road.road_objects.update({len(my_road.road_objects): new_object})
    return my_road


def create_structural_object(polyline, object_type, height=0.0):
    new_structural_object = StructuralObject(polyline=polyline, type=object_to_structural_object_mapping(object_type))
    new_structural_object.height = height
    return new_structural_object


def create_lateral_marking(polyline, odr_object, long_size):
    if object_to_marking_mapping(odr_object.type) == ReferenceTypes.LateralMarkingType.UNKNOWN:
        return

    if odr_object.markings:
        color = lateral_marking_color_mapping(odr_object.marking.color)
    else:
        color = ReferenceTypes.LateralMarkingColor.WHITE

    new_lateral_marking = LateralMarking(polyline=polyline, type=object_to_marking_mapping(odr_object.type),
                                         long_size=long_size, color=color)

    return new_lateral_marking


def create_boundary_from_object(my_road, center_line_points, lookup_table, odr_object, index, vvm_road_id, polyline):
    # lookup_table = np.array([])   -->  road id || lanesection || laneID || road id VVM || lane id VVM

    # object.s is always the starting point index of the boundary
    # object.length defines the length along s-axis
    if odr_object.length:
        object_ending_s_index = odr_object.s + odr_object.length

    # for repeat objects the length may vary from global definition
    if odr_object.repeat:
        if len(odr_object.repeat) == 1:
            # one single repeat definition - as visualized in the open drive documentation
            if odr_object.repeat[0].length:
                object_ending_s_index = odr_object.s + odr_object.repeat[0].length
        else:
            # multiple object repeat - as seen in real data
            if odr_object.repeat[len(odr_object.repeat) - 1].length:
                object_ending_s_index = odr_object.repeat[len(odr_object.repeat) - 1].s +\
                                   odr_object.repeat[len(odr_object.repeat) - 1].length

    my_boundary = Boundary()
    # type, material, color Mapping
    my_boundary.type = object_to_boundary_mapping(odr_object.type)
    my_boundary.condition = 0x0
    my_boundary.height = 0x0
    my_boundary.subtype = 0x0
    my_boundary.color = 0x0

    # get start index
    for l in range(0, len(center_line_points) - 1):
        if center_line_points[l, 0] <= odr_object.s < center_line_points[l + 1, 0]:
            my_boundary.poly_index_start = l
            break

    # get end index
    for l in range(0, len(center_line_points) - 1):
        # end point = start point of next road mark
        if center_line_points[l, 0] <= object_ending_s_index < center_line_points[l + 1, 0]:
            my_boundary.poly_index_end = l
            break

    # t is defined positive towards the left side of a road, zero is in center of road
    central_boundary = False
    if odr_object.t == 0:
        central_boundary = True
    elif odr_object.t < 0:
        my_boundary.is_right_boundary = True
    else:
        my_boundary.is_right_boundary = False

    if odr_object.height:
        my_boundary.height = odr_object.height

    boundary_table = find_boundary_lanes(lookup_table, central_boundary, my_boundary.is_right_boundary, index,
                                         vvm_road_id)

    if boundary_table:
        my_road = append_boundary_to_lane(my_road, boundary_table, my_boundary, central_boundary)
    else:
        # fallback if no matching lane was found
        new_object = RoadObject(polyline=polyline, type=ReferenceTypes.RoadObjectType.CRASH_ABSORBER,
                                height=my_boundary.height)
        new_object.drivable = False
        new_object.walkable = False
        my_road.road_objects.update({len(my_road.road_objects): new_object})

    return my_road


def append_boundary_to_lane(my_road, boundary_table, my_boundary, central_boundary):
    """
    Append the boundary to the lane:
    In omega a road can have multiple boundaries. Usually one lane would have a road mark as boundary, but can
    have some sort of barrier as a secondary boundary. Therefore we simply add the created boundary to the lane.
    """
    # boundary_table = odr_lane_id || omega_road_id || omega_lane_id || is_right_lane
    for entry in boundary_table:
        for l_nr, lane in enumerate(my_road.lanes):
            if entry[2] == l_nr:

                if central_boundary:
                    if entry[4]:
                        my_boundary.is_right_boundary = True
                    else:
                        my_boundary.is_right_boundary = False

                my_road.lane[l_nr].boundary.update({len(my_road.lane[0].boundary): my_boundary})

    return my_road


def find_boundary_lanes(lookup_table, is_central_boundary, is_right_boundary, section_index, vvm_road_id):
    # lookup_table = road id || lanesection || laneID || road id VVM || lane id VVM
    # boundary_table = odr_lane_id || omega_road_id || omega_lane_id || right_lane
    boundary_table = []

    for i, entry in enumerate(lookup_table):
        if entry[3] != vvm_road_id:
            # if not current road step over
            continue

        if i < len(lookup_table) - 1:
            next_entry = lookup_table[i + 1]
            if section_index == entry[1] and section_index == next_entry[1]:
                # the highest absolute number of opendrive lane ids is the most outer lane of the road
                # to which the object has to be appended

                if is_right_boundary:
                    if entry[2] < 0 and next_entry[2] < 0:
                        # right lanes have indices < 0
                        if entry[2] < next_entry[2]:
                            boundary_table.append([entry[2], entry[3], entry[4], True])
                else:
                    if entry[2] > 0 and next_entry[2] > 0:
                        # left lanes have indices > 0
                        if entry[2] > next_entry[2]:
                            boundary_table.append([entry[2], entry[3], entry[4], False])

                if is_central_boundary:
                    if int(entry[2]) == 1:
                        boundary_table.append([entry[2], entry[3], entry[4], False])

                    if int(entry[2]) == -1:
                        boundary_table.append([entry[2], entry[3], entry[4], True])

    return boundary_table


def process_object(my_road, center_line_points, odr_object, lookup_table, index, vvm_road_id, step_size):
    # repeat objects: (have a separate calculation for their geometries and are passed through)
    if odr_object.repeat:
        my_road = convert_object_repeat(my_road, center_line_points, odr_object, lookup_table, index, vvm_road_id,
                                        step_size)
        return my_road

    # all other objects:
    else:
        # borders - only represents objects borders
        if odr_object.borders:
            """
            In OpenDrive Objects can have a separate border defined in object.borders. This is not transferable into
            OMEGAFormat usually. Maybe some detailed information of the object can be extracted through the border.
            """
            pass

        # validity
        if odr_object.validity:
            """
            In OpenDrive Objects can be rendered to be valid for specific lanes only. For objects this is not
            provided in OMEGAFormat.
            """
            pass

        # get center point
        object_center_point = calculate_object_center_point(odr_object.s, center_line_points, t=odr_object.t,
                                                            hdg=odr_object.hdg, z_offset=odr_object.z_offset)

        # outline(s)
        outlines = []
        if odr_object.outline is not None:
            outlines.append(odr_object.outline)
        if odr_object.outlines is not None:
            if odr_object.outlines.objectOutlines:
                for outline in odr_object.outlines.objectOutlines:
                    outlines.append(outline)

        # calculate corresponding polyline
        polyline = calculate_polyline(center_line_points, object_center_point, length=odr_object.length,
                                      width=odr_object.width, radius=odr_object.radius, outlines=outlines, object_id=odr_object.id)

        # objects height
        height = 0
        if odr_object.height is not None:
            height = odr_object.height
        elif outlines:
            height = get_outlines_max_height(outlines)

        # convert object
        my_road = convert_object(my_road, odr_object, center_line_points, lookup_table, vvm_road_id, index, polyline,
                                 height)

    return my_road


def convert_object_repeat(my_road, center_line_points, odr_object, lookup_table, index, vvm_road_id, step_size):
    """
    *   the documentation shows a case where you would define one single object repeat which in reality
        is a few fragmented objects
    *   actual map data uses multiple repeat objects to describe rails and noise-guards
    *   variables defined by a starting- and ending- value will be interpolated for a finite quantity of elements.
        For those elements that have a quantity of 1 (that are continuous) the interpolation is made in the
        wanted resolution of the polyline.
    *   variable values for height can not be adopted, because in omega we only have one height value per object
    """

    # one single repeat definition - as visualized in the open drive documentation
    if len(odr_object.repeat) == 1:

        if odr_object.repeat[0].distance and odr_object.repeat[0].distance != 0:
            # for multiple fragmented objects
            my_road = fragment_object_repeat(my_road, odr_object, center_line_points, lookup_table, index, vvm_road_id)
            return my_road
        else:
            # for a single continuous object
            my_road = continuous_object_repeat(my_road, odr_object, center_line_points, lookup_table, index,
                                               vvm_road_id, step_size)
            return my_road
    else:
        # multiple object repeat - as seen in real data
        my_road = multiple_object_repeat(my_road, odr_object, center_line_points, lookup_table, index, vvm_road_id)

    return my_road


def multiple_object_repeat(my_road, odr_object, center_line_points, lookup_table, index, vvm_road_id):
    # i is the number of "object_repeat"-objects definitions
    # and not the number of "object-repeats"-objects quantity as you would see in the documentation

    # loop through
    for i in range(0, len(odr_object.repeat)):
        # mandatory
        s = odr_object.repeat[i].s
        length = odr_object.repeat[i].length
        distance = odr_object.repeat[i].distance
        t_start = odr_object.repeat[i].t_start
        t_end = odr_object.repeat[i].t_end
        height = max(odr_object.repeat[i].height_start, odr_object.repeat[i].height_end)
        height_start = odr_object.repeat[i].height_start
        height_end = odr_object.repeat[i].height_end
        z_offset_start = odr_object.repeat[i].z_offset_start
        z_offset_end = odr_object.repeat[i].z_offset_end
        # optional
        width_start = odr_object.repeat[i].width_start
        width_end = odr_object.repeat[i].width_end
        length_start = odr_object.repeat[i].length_start
        length_end = odr_object.repeat[i].length_end
        radius_start = odr_object.repeat[i].radius_start
        radius_end = odr_object.repeat[i].radius_end

        if distance > 0.0:
            quantity = length / distance

            for j in range(0, quantity):
                # mandatory
                current_s = s + j * distance
                t = interpolate_linear(t_start, t_end, 0, quantity, j)
                z_offset = interpolate_linear(z_offset_start, z_offset_end, 0, quantity, j)
                height = interpolate_linear(height_start, height_end, 0, quantity, j)
                center_point = calculate_object_center_point(current_s, center_line_points, t=t, hdg=0.0,
                                                             z_offset=z_offset)

                # depending on shape fill with not None value
                radius = None
                length_local = None
                width = None

                if radius_start and radius_end:
                    radius = interpolate_linear(radius_start, radius_end, 0, quantity, j)

                if length_start and length_end:
                    length_local = interpolate_linear(length_start, length_end, 0, quantity, j)

                if width_start and width_end:
                    width = interpolate_linear(width_start, width_end, 0, quantity, j)

                # calculate polyline decides which shape, according to given not None values
                polyline = calculate_polyline(center_line_points, center_point, length=length_local, width=width,
                                              radius=radius, outlines=[], object_id=odr_object.id)
                if polyline:
                    my_road = convert_object(my_road, odr_object, center_line_points, lookup_table, vvm_road_id, index,
                                             polyline, height)

            continue

        # no distance - no fragmentization
        # radial
        if radius_start is not None and radius_end is not None:
            radius = (radius_start + radius_end) * 0.5
            center_point = calculate_object_center_point(s + length * 0.5, center_line_points, t=t_start, hdg=0.0,
                                                         z_offset=z_offset_start)
            polyline = calculate_polyline(center_line_points, center_point, length=None, width=None, radius=radius, object_id=odr_object.id,
                                          outlines=[])

            if polyline:
                check_polyline(polyline)
                my_road = convert_object(my_road, odr_object, center_line_points, lookup_table, vvm_road_id, index,
                                         polyline, height)
                continue

        if width_start is not None and width_end is not None:
            width_start = width_start
            width_end = width_end
            center_point_start = calculate_object_center_point(s, center_line_points, t=t_start, hdg=0.0,
                                                               z_offset=z_offset_start)
            center_point_end = calculate_object_center_point(s + length, center_line_points, t=t_end, hdg=0.0,
                                                             z_offset=z_offset_end)

            # fences and noise walls
            if width_start == 0.0 and width_end == 0.0:
                polyline_list = []
                polyline_list.append(get_polyline_from_point(center_point_start))
                polyline_list.append(get_polyline_from_point(center_point_end))
                polyline = create_polyline_from_list(polyline_list, polyline_list[0].pos_x.shape[0])
            else:
                polyline = get_polyline_for_rect_obj_repeat(center_point_start, center_point_end, width_start, width_end)

            if polyline:
                check_polyline(polyline)
                my_road = convert_object(my_road, odr_object, center_line_points, lookup_table, vvm_road_id, index,
                                         polyline, height)

    return my_road


def fragment_object_repeat(my_road, odr_object, center_line_points, lookup_table, index, vvm_road_id):
    # general calculations:
    length = odr_object.repeat[0].length
    s_start = odr_object.repeat[0].s
    distance = odr_object.repeat[0].distance
    quantity = int(length / distance)

    # optional
    width_start = odr_object.repeat[0].width_start
    width_end = odr_object.repeat[0].width_end
    length_start = odr_object.repeat[0].length_start
    length_end = odr_object.repeat[0].length_end
    radius_start = odr_object.repeat[0].radius_start
    radius_end = odr_object.repeat[0].radius_end
    radius = None
    width = None
    length_local = None

    for j in range(0, quantity):
        # current_s
        current_s = s_start + (length / quantity) * j
        t = interpolate_linear(odr_object.repeat[0].t_start, odr_object.repeat[0].t_end, 0, quantity, j)
        z_offset = interpolate_linear(odr_object.repeat[0].z_offset_start, odr_object.repeat[0].z_offset_end, 0, quantity, j)
        height = interpolate_linear(odr_object.repeat[0].height_start, odr_object.repeat[0].height_end, 0, quantity, j)

        if radius_start is not None and radius_end is not None:
            radius = interpolate_linear(radius_start, radius_end, 0, quantity, j)

        if length_start is not None and length_end is not None:
            length_local = interpolate_linear(length_start, length_end, 0, quantity, j)

        if width_start is not None and width_end is not None:
            width = interpolate_linear(width_start, width_end, 0, quantity, j)

        # calculate the polyline depending on above calculated values
        object_center_point = calculate_object_center_point(current_s, center_line_points, t=t, hdg=None,
                                                            z_offset=z_offset)
        polyline = calculate_polyline(center_line_points, object_center_point, length=length_local, width=width,
                                      radius=radius, object_id=odr_object.id)

        if polyline:
            check_polyline(polyline)
            my_road = convert_object(my_road, odr_object, center_line_points, lookup_table, vvm_road_id, index,
                                     polyline, height)

    return my_road


def continuous_object_repeat(my_road, odr_object, center_line_points, lookup_table, index, vvm_road_id, step_size):
    polyline_list = []

    length = odr_object.repeat[0].length
    s_start = odr_object.repeat[0].s
    height = max(odr_object.repeat[0].height_start, odr_object.repeat[0].height_end)
    z_offset = 0.0
    # radius - doesn't make sense for a single continuous object
    width = None

    step = step_size  # m between each point
    if length is None or length < step:
        quantity = 1
    else:
        quantity = int(math.ceil(length / step))

    for j in range(0, quantity):
        current_s = s_start + (length / quantity) * j
        t = interpolate_linear(odr_object.repeat[0].t_start, odr_object.repeat[0].t_end, 0, quantity, j)
        if odr_object.repeat[0].z_offset_end:
            z_offset = interpolate_linear(odr_object.repeat[0].z_offset_start,
                                          odr_object.repeat[0].z_offset_end, 0, quantity, j)
        elif odr_object.z_offset[0]:
            z_offset = odr_object.z_offset

        # width:
        if odr_object.repeat[0].width_start and odr_object.repeat[0].width_end:
            width = interpolate_linear(odr_object.repeat[0].width_start, odr_object.repeat[0].width_end, 0, quantity, j)

        # center point for step
        object_center_point = calculate_object_center_point(current_s, center_line_points, t=t, hdg=None,
                                                            z_offset=z_offset)

        if width:
            step_polyline = get_polyline_from_width(object_center_point, width)
        else:
            step_polyline = get_polyline_from_point(object_center_point)

        if step_polyline.pos_x[0] != 0.0:
            polyline_list.append(step_polyline)

    if polyline_list:
        polyline = create_polyline_from_list(polyline_list, polyline_list[0].pos_x.shape[0])
    else:
        logger.warning("No polyline in continuous object repeat!")
        return my_road

    if polyline:
        check_polyline(polyline)
        my_road = convert_object(my_road, odr_object, center_line_points, lookup_table, vvm_road_id, index, polyline,
                                 height)

    return my_road
