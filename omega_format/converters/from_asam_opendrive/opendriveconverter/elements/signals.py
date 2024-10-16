import math
from omega_format import Sign, Position, Lane, LateralMarking, FlatMarking, ReferenceTypes, ReferenceDict
from ..logger import logger
from .mapping import signal_type_mapping, signal_to_flat_marking_mapping, signal_to_lateral_marking_mapping, \
    signal_shape_mapping, signal_fallback_master_mapping, signal_fallback_slave_mapping
from .polyline import calculate_object_center_point, get_polyline_from_width


def get_road_signals(my_road, road, center_line_points, lookup_table, reference_table, vvm_road_id):
    # reference_table = [omega signal id | omega road id | odr signal id | reference id (odr) | connected_to id (odr)]

    if road.signals is not None:

        # Signal
        if road.signals.signal is not None:
            for signal in road.signals.signal:
                my_road, reference_table = convert_signal(my_road, center_line_points, signal, lookup_table,
                                                          reference_table, vvm_road_id)

        # Signal Reference
        if road.signals.signal_reference is not None:
            for signal_reference in road.signals.signal_reference:
                my_road, reference_table = process_signal_reference(my_road, center_line_points, signal_reference,
                                                                    reference_table, lookup_table, vvm_road_id)

        # fallback detection via position
        my_road = process_fallback_via_distance(my_road)

    return my_road, reference_table


def process_fallback_via_distance(my_road):
    """
    Evaluates if a sign is a fallback - e.g. priorities when traffic lights are off
    :param my_road:
    :return:
    """
    for first_sign in my_road.signs.values():

        # check if signal type qualifies for fallback option
        if signal_fallback_master_mapping(first_sign.type):

            # iterate over all signals of road again to find possible connected signs
            for i, second_sign in enumerate(my_road.signs.values()):

                # check if secondary sign qualifies for fallback option
                if signal_fallback_slave_mapping(second_sign.type):

                    # check for similar position by calculating squared distance
                    delta_x = first_sign.position.pos_x - second_sign.position.pos_x
                    delta_y = first_sign.position.pos_y - second_sign.position.pos_y
                    sqrd_dist = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))
                    if sqrd_dist < 1.0:
                        my_road.signs[i].fallback = True

    return my_road


def process_signal_reference(my_road, center_line_points, signal_reference, reference_table, lookup_table,
                             vvm_road_id):

    position, hdg = calculate_signal_position_simple(center_line_points, signal_reference.s, signal_reference.t)

    if position is None:
        logger.warning('Failure while calculating signal_reference position. Element is dropped.')
        return my_road, reference_table

    applicable_lanes_vvm = find_applicable_lanes(lookup_table, vvm_road_id, signal_reference.orientation,
                                                 signal_reference.validity)

    # information is updated from referenced signal later in process
    new_signal = create_new_signal(position, hdg, applicable_lanes_vvm, ReferenceTypes.SignType.UNKNOWN,
                                   signal_size=0, signal_value=0, dynamic=False)
    if new_signal is not None:
        my_road.signs.update({len(my_road.signs): new_signal})
        reference_table.append([len(my_road.signs)-1, vvm_road_id, None, signal_reference.id, None])

    return my_road, reference_table


def convert_signal(my_road, center_line_points, signal, lookup_table, reference_table, vvm_road_id):
    # reference_table = [omega signal id | omega road id | odr signal id | reference id (odr) | connected_to id (odr)]
    position, hdg = calculate_signal_position(center_line_points, signal)
    center_point = [position.pos_x, position.pos_y, hdg, position.pos_z]

    if position is None:
        logger.warning(f'Failure while calculating signals position. Signal with id {signal.id} is dropped.')
        return my_road, reference_table

    applicable_lanes_vvm = find_applicable_lanes(lookup_table, vvm_road_id, signal.orientation, signal.validity)

    if signal.country is None:
        logger.warning(f'Only the german signal catalog can be converted.'
              f'Signal with id {signal.id} has no country code: german is assuemd!')
    elif signal.country.lower() in ["germany", "de", "deu", "german", "opendrive"]:
        pass
    else:
        logger.warning(f'Only the german signal catalog can be converted.'
              f'Signal with id {signal.id} has country code: {signal.country}')

    # add subtype to type, if not available add "-1"
    if signal.name is not None and 'Sign' in signal.name:
        total_type = signal.name.split('_')[1]
    elif signal.type:
        if signal.subtype:
            if signal.subtype[0] == "-":    # sometimes "-" is included in subtype sometimes not
                total_type = signal.type.lower() + signal.subtype.lower()
            else:
                total_type = signal.type.lower() + "-" + signal.subtype.lower()
        else:
            total_type = signal.type.lower() + "-1"


    # find mapping
    if signal_type_mapping(total_type) is not None:
        signal_type = signal_type_mapping(total_type)

        # find signal size rough
        signal_size = set_signal_size(my_road.location, signal_type)

        # time-/ or weather dependent?
        dynamic = False
        if signal.dynamic != "no":
            dynamic = True

        new_signal = create_new_signal(position, hdg, applicable_lanes_vvm, signal_type, signal_size, signal.value,
                                       dynamic)
        if new_signal is not None:
            my_road.signs.update({len(my_road.signs): new_signal})

            if signal.reference:
                for reference in signal.reference:
                    reference_table.append([len(my_road.signs)-1, vvm_road_id, signal.id, None, reference.id])
            else:
                reference_table.append([len(my_road.signs)-1, vvm_road_id, signal.id, None, None])

            # historical sign?
            if signal.country_revision:
                if int(signal.country_revision < 2017):
                    my_road.signs[len(my_road.signs)-1].history = str(signal.country_revision) + " " + str(total_type)

    # flat marking
    elif signal_to_flat_marking_mapping(total_type) is not None:
        flat_marking_type = signal_to_flat_marking_mapping(total_type)
        new_flat_marking = create_flat_marking_from_signal(center_point, flat_marking_type, signal)
        if new_flat_marking is not None:
            if applicable_lanes_vvm:
                for lane in applicable_lanes_vvm:
                    if lane in my_road.lanes:
                        my_road.lanes[lane].flat_markings.update(
                            {len(my_road.lanes[lane].flat_markings): new_flat_marking})
                        # references are only possible between two signs, so no need to include flat marking to
                        # reference_table

    # lateral marking
    elif signal_to_lateral_marking_mapping(total_type) is not None:
        lateral_marking_type = signal_to_lateral_marking_mapping(total_type)
        new_lateral_marking = create_lateral_marking_from_signal(center_point, lateral_marking_type, signal,
                                                                 applicable_lanes_vvm)
        if new_lateral_marking is not None:
            my_road.lateral_markings.update({len(my_road.lateral_markings): new_lateral_marking})
            # references are only possible between two signs, so no need to include lateral marking to reference_table

    return my_road, reference_table


def create_new_signal(signal_position, hdg, applicable_lanes, signal_type, signal_size, signal_value, dynamic):

    if not applicable_lanes:
        applicable_lanes = ReferenceDict([], Lane)
    else:
        applicable_lanes = ReferenceDict(applicable_lanes, Lane)

    value = 0
    if signal_value:
        value = signal_value

    if signal_position is not None:
        new_signal = Sign(type=signal_type, value=value, history="0", applicable_lanes=applicable_lanes,
                          position=signal_position, heading=hdg, size_class=signal_size)
        new_signal.weather_dependent = dynamic
        new_signal.time_dependent = dynamic
        return new_signal
    else:
        return None


def create_flat_marking_from_signal(center_point, flat_marking_type, signal):
    # keepout area and zig-zag could be defined as signals, but signals only have a width, polyline would be linear!
    if signal.width is not None:
        polyline = get_polyline_from_width(center_point, signal.width)
    else:
        # generic width is used, because polyline of two points is mandatory
        polyline = get_polyline_from_width(center_point, 0.5)

    new_flat_marking = FlatMarking(polyline=polyline, type=flat_marking_type, value=0x0,
                                   color=ReferenceTypes.LateralMarkingColor.UNKNOWN)

    return new_flat_marking


def create_lateral_marking_from_signal(center_point, lateral_marking_type, signal, applicable_lanes):
    if signal.width is not None:
        polyline = get_polyline_from_width(center_point, signal.width)
    else:
        # generic width is used, because polyline of two points is mandatory
        polyline = get_polyline_from_width(center_point, 2.5)

    applicable_lanes = ReferenceDict(applicable_lanes, Lane)
    new_lateral_marking = LateralMarking(polyline=polyline, type=lateral_marking_type, long_size=0.0,
                                         color=ReferenceTypes.LateralMarkingColor.UNKNOWN,
                                         applicable_lanes=applicable_lanes)

    return new_lateral_marking


def find_applicable_lanes(lookup_table, vvm_road_id, orientation=None, validity=None):
    # lookup_table: [opendrive_road_id, opendrive_lanesection_id, opendrive_lane_id, vvm_road_id, vvm_lane_id)]
    applicable_lanes_vvm = []
    """
    -   Driving along a road corresponds to increasing the value of s. If a sign shows up it will be
        valid (from this point until it is overridden or comparable event) for the whole lane.
    -   Validity references which lanes are affected by the signal.
    -   TODO: Some signals are defined with an s-value higher then that of the road. The reason is not sure, but maybe
        we should find successors and predecessors of these roads to assign signals rules to the street. On the other
        hand it might be a problem with the editors, assigning the sign to the wrong road - in which case we can not
        heal the mismatch. 
        for lane_section in road.lanes.lane_section:
                if signal.s > lane_section.s
    """
    for row in lookup_table:
        if row[3] == vvm_road_id:
            # when lane is already inside list, skip step
            if row[4] in applicable_lanes_vvm:
                continue
            # when orientation is set (and no validity), append according to its definition
            if orientation and not validity:
                if orientation == "+":
                    # for right hand-traffic a positive orientation "+" is along the s-value, lane numbers are negative
                    if row[2] < 0:
                        applicable_lanes_vvm.append((vvm_road_id, row[4]))
                elif orientation == "-":
                    # for right-hand traffic negative orientation "-" is against the s-value, lane numbers are positive
                    if row[2] > 0:
                        applicable_lanes_vvm.append((vvm_road_id, row[4]))

            # when validity is set, append following its definition
            elif validity:
                for validity_entry in validity:
                    if validity_entry.from_lane == 0 and validity_entry.to_lane == 0:
                        # lane 0 is the centerline, some data seems to be defined wrong here
                        applicable_lanes_vvm.append((vvm_road_id, row[4]))
                    elif validity_entry.from_lane <= row[2] <= validity_entry.to_lane:
                        applicable_lanes_vvm.append((vvm_road_id, row[4]))

            # for any other case the signal will be valid for all lanes
            else:
                applicable_lanes_vvm.append((vvm_road_id, row[4]))

    return applicable_lanes_vvm


def calculate_signal_position(center_line_points, signal):
    # center_line_points is a 6-dimensional list: [s, x, y, heading, z, superelevation]
    hdg = 0.0
    if signal.orientation == "-":   # "-" means, the signal is valid/orientated in negative s direction
        hdg = math.pi

    if signal.h_offset is not None:
        hdg = hdg + signal.h_offset

    if signal.physical_position is not None:

        if signal.physical_position.position_road is not None:
            s = signal.physical_position.position_road.s
            t = signal.physical_position.position_road.t
            z_offset = signal.physical_position.position_road.z_offset

            signal_center_point = calculate_object_center_point(s, center_line_points, t=t, hdg=0.0, z_offset=z_offset)
            position = Position(pos_x=signal_center_point[0], pos_y=signal_center_point[1],
                                pos_z=signal_center_point[3])
            return position, signal_center_point[2]+hdg

        if signal.physical_position.position_inertial is not None:
            position = Position(pos_x=signal.physical_position.position_inertial.x,
                                pos_y=signal.physical_position.position_inertial.y,
                                pos_z=signal.physical_position.position_inertial.z)
            return position, (signal.physical_position.position_inertial.hdg + hdg)

    # no physical position element
    else:
        return calculate_signal_position_simple(center_line_points, signal.s, signal.t, hdg, signal.z_offset)


def calculate_signal_position_simple(center_line_points, s, t, hdg=None, z_offset=None):
    signal_center_point = calculate_object_center_point(s, center_line_points, t, hdg=hdg,
                                                        z_offset=z_offset)

    position = Position(pos_x=signal_center_point[0], pos_y=signal_center_point[1], pos_z=signal_center_point[3])

    hdg_total = signal_center_point[2]
    if hdg:
        hdg_total = signal_center_point[2] + hdg

    return position, hdg_total


def set_signal_size(location, signal_type):
    # shape = 0 is round, 1 is angled
    signal_shape = signal_shape_mapping(signal_type)
    signal_size = 0  # unknown

    if location == ReferenceTypes.RoadLocation.HIGHWAY:
        signal_size = 3
    elif location == ReferenceTypes.RoadLocation.NON_URBAN and signal_shape == 0:
        signal_size = 3
    elif location == ReferenceTypes.RoadLocation.NON_URBAN and signal_shape == 1:
        signal_size = 2
    elif location == ReferenceTypes.RoadLocation.URBAN:
        signal_size = 1

    return signal_size


def setup_signal_references(my_roads, reference_table):
    # reference_table = [omega signal id | omega road id | odr signal id | reference id (odr) | connected_to id (odr)]
    for row in reference_table:
        # when a signalReference is found - copy data from original signal
        if row[3]:
            # look for the original signal
            for search_row in reference_table:
                if search_row[2] == row[3]:
                    # copy the referenced signals data into the referencing one
                    referenced_signal = my_roads.roads_list[search_row[1]].signs[search_row[0]]
                    my_roads.roads_list[row[1]].signs[row[0]].type = referenced_signal.type
                    my_roads.roads_list[row[1]].signs[row[0]].size_class = referenced_signal.size_class
                    my_roads.roads_list[row[1]].signs[row[0]].value = referenced_signal.value

        # when a reference is found: set the connected_to attribute
        if row[4]:
            # search for connected signal
            for search_row in reference_table:
                if search_row[2] == row[4]:
                    # for first element
                    connected_to = ReferenceDict((search_row[1], search_row[0]), Sign())
                    my_roads.roads_list[row[1]].signs[row[0]].connected_to = connected_to
                    # for second element (needs to be connected vice versa)
                    connected_to = ReferenceDict((row[1], row[0]), Sign())
                    my_roads.roads_list[search_row[1]].signs[search_row[0]].connected_to = connected_to

                    # check if first element is 'master'
                    if signal_fallback_master_mapping(my_roads.roads_list[search_row[1]].signs[search_row[0]].type):

                        # check if secondary sign qualifies as fallback
                        if signal_fallback_slave_mapping(my_roads.roads_list[row[1]].signs[row[0]].type):
                            my_roads.roads_list[row[1]].signs[row[0]].fallback = True

    return my_roads
