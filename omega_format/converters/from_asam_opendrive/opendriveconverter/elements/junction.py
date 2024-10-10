from omega_format import Lane, ReferenceElement
from ..logger import logger

def setup_connections(my_roads, lookup_table, my_opendrive):
    """
    1. go through my_opendrive roads again
    2.  find linkage element per road: either junction with certain number or opendrive road id. If no linkage
        element is provided within the road, the lanes can still have linkage elements. We are assuming that those are
        then linked within the same road, but with a different lane section of that road
    2a: if junction: all combinations including the current road id are searched and saved incl. there from and to lanes
    3.  go through all lanes of that road and find current lane in lookup table --> determine VVM road and lane ids for
        that lane
    4a. no predecessor or successor has been set for the road, but predecessor or successor found for a lane
        --> search within own road, but different lane section
        4a.1 find the successor and predecessor in the lookup table
             if looking for successor go forwards in own lane sections
             if looking for predecessor go backwards in own lane section
             if correct lane numbers can not be found by going one step forwards/backwards, look recursively in own
             road (but do not output current lane section)
             --> find their VVM ids
        4a.2 insert VVM ids to VVM current lane as successor or predecessor
    4b. if no junction: find successor and predecessor of lane in openDrive (include road successor and predecessor
        determined in 2.)
        4b.1 find the successor and predecessor in the lookup table
        (starts with lane section 0 if looking for a successor, since current road should be connected to beginning of
        other road in case of successor, if it cant find the combination it increases the lane section number)
            --> find their VVM ids
        (starts with lane section maximum if looking for a predecessor, since current road should be connected to end of
        other road in case of predecessor, if it cant find the combination it increases the lane section number)
            --> find their VVM ids
        4b.2 insert VVM ids to VVM current lane as successor or predecessor
    4c. if junction: all combinations with current road id incl. from and to lane numbers have been saved in 2a
        4c.1 the current lane is searched for --> road and lane id of connecting road is searched in lookuptable
        --> find their VVM ids
        4c.2 insert VVM ids to VVM current lane as successor or predecessor

    # get other information per road (use lookup table) once roads and lanes have been inserted in VVM format
    # (e.g. predecessors/successors etc.)
    # get each road
    :param my_roads:
    :param lookup_table:
    :param my_opendrive:
    :return:
    """

    for road in my_opendrive.roads:
        # get road id in opendrive
        opendrive_road_id = road.id
        predecessor_exists_global = False
        predecessor_junction_global = False
        successor_exists_global = False
        successor_junction_global = False

        if road.link.predecessor is not None:
            predecessor_exists_global = True
            # check if road or junction
            if road.link.predecessor.element_type == 'road':
                road_predecessor = road.link.predecessor.element_id
            elif road.link.predecessor.element_type == 'junction':
                # need to find current opendrive_road_id in connections and find connecting road
                connection_road_lane_list_predecessor = find_junction(opendrive_road_id,
                                                                      road.link.predecessor.element_id, my_opendrive)
                predecessor_junction_global = True
                if not connection_road_lane_list_predecessor:
                    # oneway streets going out of a junction are not defined, so it is not necessarily bad
                    pass
            else:
                logger.error('Unknown road linkage type')

        if road.link.successor is not None:
            successor_exists_global = True
            if road.link.successor.element_type == 'road':
                road_successor = road.link.successor.element_id
            elif road.link.successor.element_type == 'junction':
                # need to find current opendrive_road_id in connections and find connecting road
                connection_road_lane_list_successor = find_junction(opendrive_road_id, road.link.successor.element_id,
                                                                    my_opendrive)
                successor_junction_global = True
                if not connection_road_lane_list_successor:
                    # oneway streets going out of a junction are not defined, so it is not necessarily bad
                    pass
            else:
                logger.error('Unknown road linkage type')

        # go over all lane sections
        for section_count, lane_section in enumerate(road.lanes.lane_section):
            sides = dict(
                left=lane_section.left_lanes,
                right=lane_section.right_lanes,
            )
            # check if more than one lane section and in which we are in
            if len(road.lanes.lane_section) > 1:
                # if lane section == 0 (start: predecessor stays the same, successor is set to false
                # (if set to false the tool checks for predecessor/successor in the own road, but in  a
                # different lane section))
                if section_count == 0:
                    successor_exists = False
                    successor_junction = False
                    predecessor_exists = predecessor_exists_global
                    predecessor_junction = predecessor_junction_global
                # if >1 lane section and in lane section >0 and not in last
                # --> successor and predecessor need to be set to false
                elif section_count > 0 and section_count != len(road.lanes.lane_section) - 1:
                    successor_exists = False
                    successor_junction = False
                    predecessor_exists = False
                    predecessor_junction = False
                # if lane section last --> successor is kept, predecessor is set to false
                elif section_count == len(road.lanes.lane_section) - 1:
                    successor_exists = successor_exists_global
                    successor_junction = successor_junction_global
                    predecessor_exists = False
                    predecessor_junction = False
            # only one lane section --> everything stays unaltered
            else:
                # set local to global
                successor_exists = successor_exists_global
                successor_junction = successor_junction_global
                predecessor_exists = predecessor_exists_global
                predecessor_junction = predecessor_junction_global

            # get each lane of the road (center lane not connected) for each side
            for side_flag, lanes_of_side in sides.items():
                # get each lane of side
                for i in range(0, len(lanes_of_side)):
                    # find corresponding entry in lookup_table (runs with correct lane section)
                    # --> find VVM id of current lane
                    row_number_origin = lookup_table_search_precisely(opendrive_road_id, section_count,
                                                                      lanes_of_side[i].id, lookup_table)
                    if row_number_origin is None:
                        logger.warning('For some reason the correct road_id, section_id and lane_id set could not be '
                              'identified in the lookup_table')
                    else:
                        # get correct VVM road and lane id
                        vvm_road_id = lookup_table[row_number_origin][3]
                        vvm_lane_id = lookup_table[row_number_origin][4]
                        # get link element
                        # predecessor
                        if lanes_of_side[i].link.predecessor:
                            for predecessor in lanes_of_side[i].link.predecessor:
                                # find this combination in lookup table

                                # There can be lane linkage elements without having a road linkage element --> we are
                                # assuming that in those cases the lane is linked to another lane of the same road in a
                                # different lane section
                                if not predecessor_exists:
                                    row_number_predecessor = lookup_table_search_section(opendrive_road_id,
                                                                                         section_count,
                                                                                         section_count - 1, predecessor,
                                                                                         lookup_table, True)
                                # no good method to find correct lane section number straight away. Therefore method is
                                # looking recursively, probably should not be junction and contain in formation in the
                                # lane link element at the same time
                                elif not predecessor_junction:
                                    # predecessor is connected at its end --> search for max lane section
                                    max_lane_section = find_max_lane_section(road_predecessor, lookup_table)
                                    row_number_predecessor = lookup_table_search(road_predecessor, max_lane_section,
                                                                                 predecessor, lookup_table, True)

                                my_roads = set_predecessor(row_number_predecessor, my_roads, vvm_road_id, vvm_lane_id,
                                                           side_flag, lookup_table)
                        # if part of junction: each lane usually does not contain successor/predecessor in lane link.
                        # it is noted in connection. which is read previously
                        elif predecessor_junction:
                            # search in connection_road_lane_list_predecessor list
                            for row_junction_lookup in connection_road_lane_list_predecessor:

                                if row_junction_lookup[1] == lanes_of_side[i].id:
                                    max_lane_section = find_max_lane_section(row_junction_lookup[0], lookup_table)
                                    row_number_predecessor = lookup_table_search(row_junction_lookup[0],
                                                                                 max_lane_section,
                                                                                 row_junction_lookup[2], lookup_table,
                                                                                 True)

                                    my_roads = set_predecessor(row_number_predecessor, my_roads, vvm_road_id,
                                                               vvm_lane_id, side_flag, lookup_table)

                        # successors
                        if lanes_of_side[i].link.successor:
                            for successor in lanes_of_side[i].link.successor:
                                # find this combination in lookup table

                                # There can be lane linkage elements without having a road linkage element
                                # --> we are assuming that in those cases the lane is linked to another lane of the same
                                # road in a different lane section
                                if not successor_exists:
                                    row_number_successor = lookup_table_search_section(opendrive_road_id, section_count,
                                                                                       section_count + 1, successor,
                                                                                       lookup_table, True)
                                # no good method to find correct lane section number straight away. Therefore method is
                                # looking recursively
                                elif not successor_junction:
                                    # successor is connected at its beginning --> start search with lane section 0
                                    row_number_successor = lookup_table_search(road_successor, 0, successor,
                                                                               lookup_table, True)

                                my_roads = set_successor(row_number_successor, my_roads, vvm_road_id, vvm_lane_id,
                                                         side_flag, lookup_table)
                        elif successor_junction:
                            # search in connection_road_lane_list_predecessor list
                            for row_junction_lookup in connection_road_lane_list_successor:
                                if row_junction_lookup[1] == lanes_of_side[i].id:
                                    row_number_successor = lookup_table_search(row_junction_lookup[0], 0,
                                                                               row_junction_lookup[2], lookup_table,
                                                                               True)

                                    my_roads = set_successor(row_number_successor, my_roads, vvm_road_id,
                                                             vvm_lane_id, side_flag, lookup_table)

    return my_roads


def set_predecessor(row_number_predecessor, my_roads, vvm_road_id, vvm_lane_id, side_flag, lookup_table):
    # check if found
    if row_number_predecessor is not None:
        predecessor_road_id = lookup_table[row_number_predecessor][3]
        predecessor_lane_id = lookup_table[row_number_predecessor][4]
        # create reference element pointing to lane
        reference_predecessor = ReferenceElement((predecessor_road_id, predecessor_lane_id), Lane)
        vvm_lane = my_roads.roads_list.get(vvm_road_id).lanes.get(vvm_lane_id)
        # insert reference element
        # if right lanes successors should really be succesors, for left lanes successors are actually predecessors
        if side_flag == 'right':
            vvm_lane.predecessors.update({(predecessor_road_id, predecessor_lane_id): reference_predecessor})
        else:
            vvm_lane.successors.update({(predecessor_road_id, predecessor_lane_id): reference_predecessor})
    else:
        logger.warning('For some reason the correct road_id, section_id and lane_id set for the predecessor lane '
              'could not be identified in the lookup_table')
    return my_roads


def set_successor(row_number_successor, my_roads, vvm_road_id, vvm_lane_id, side_flag, lookup_table):
    # check if found
    if row_number_successor is not None:
        successor_road_id = lookup_table[row_number_successor][3]
        successor_lane_id = lookup_table[row_number_successor][4]
        # create reference element pointing to lane
        reference_successor = ReferenceElement(
            (successor_road_id, successor_lane_id), Lane)
        vvm_road = my_roads.roads_list.get(vvm_road_id)
        vvm_lane = vvm_road.lanes.get(vvm_lane_id)
        # insert reference element
        # if right lanes successors should really be successors, for left lanes successors are actually predecessors
        if side_flag == 'right':
            vvm_lane.successors.update({(successor_road_id, successor_lane_id): reference_successor})
        else:
            vvm_lane.predecessors.update({(successor_road_id, successor_lane_id): reference_successor})
    else:
        logger.warning('For some reason the correct road_id, section_id and lane_id set for the successor lane could '
              'not be identified in the lookup_table')
    return my_roads


def find_junction(opendrive_road_id, opendrive_junction_id, my_opendrive):
    """
    find junction with the opendrive junction id, look for connections of that junction that have the opendrive road id
    as input. save a list with the connecting opendrive road id and the lane linkage (to and from lane numbers in
    opendrive). No need to check the junction groups, because they only reference junction id's and nothing else.
    :param opendrive_road_id:
    :param opendrive_junction_id:
    :param my_opendrive:
    :return: list with opendrive_road_id being the incoming road and the outgoing roads for the individual lanes (incl.
            the lanes)
    """
    connection_road_lane_list = []
    for junction in my_opendrive.junctions:
        # get correct junction from my_opendrive
        if junction.id == opendrive_junction_id:
            # find all connections that have opendrive_road_id as incoming road
            for connection in junction.connection:
                if connection.incoming_road == opendrive_road_id:
                    for lane_link in connection.lane_link:
                        connection_road_lane_list.append(
                            (connection.connecting_road, lane_link.from_value, lane_link.to))

    return connection_road_lane_list


def lookup_table_search_precisely(opendrive_road_id, opendrive_lane_section_id, opendrive_lane_id, lookup_table):
    """
    look for VVM road id and VVM lane id that corresponds with the given opendrive road id, lane section id and lane id
    :param opendrive_road_id:
    :param opendrive_lane_section_id:
    :param opendrive_lane_id:
    :param lookup_table:
    :return:
    """
    counter = -1
    for row in lookup_table:
        counter += 1
        if row[0] == opendrive_road_id:
            if row[1] == opendrive_lane_section_id:
                if row[2] == opendrive_lane_id:
                    # found lane, return counter (row number)
                    return counter
    # none found --> issue warning
    logger.warning('no matching road, lanesection, lane combination found')
    return None


def lookup_table_search_section(opendrive_road_id, opendrive_lane_section_id_original, opendrive_lane_section_id_search,
                                opendrive_lane_id, lookup_table, first_run):
    """
    look for VVM road id and VVM lane id that corresponds with the given opendrive road id, lane section id_search and
    lane id.
    section search is needed if searching for the lane within the road (in different lane section)
    search should not output the original lane we are looking for predecessors/successors for in the first place
    :param opendrive_road_id:
    :param opendrive_lane_section_id_original:
    :param opendrive_lane_section_id_search:
    :param opendrive_lane_id:
    :param lookup_table:
    :param first_run:
    :return: if found, the row number, if nothing was found - nothing is returned
    """
    counter = -1
    for row in lookup_table:
        counter += 1
        if row[0] == opendrive_road_id:
            if row[1] == opendrive_lane_section_id_search and row[1] != opendrive_lane_section_id_original:
                if row[2] == opendrive_lane_id:
                    # found lane, return counter (row number)
                    return counter

    # if not found check if lane is in different lane section (work around solution, since not clear how to find out
    # beforehand in which road section lane is check if road has different lane sections
    if first_run:
        max_lane_section = find_max_lane_section(opendrive_road_id, lookup_table)
        # forward search first
        if opendrive_lane_section_id_original < opendrive_lane_section_id_search:
            # run function for all found lane sections (forward search)
            for i in range(opendrive_lane_section_id_search + 1, max_lane_section + 1):
                # forward search
                row_number = lookup_table_search_section(opendrive_road_id, opendrive_lane_section_id_original, i,
                                                         opendrive_lane_id, lookup_table,
                                                         False)
                if row_number is not None:
                    return row_number
            for i in range(opendrive_lane_section_id_search - 1, -1, -1):
                # backward search
                row_number = lookup_table_search_section(opendrive_road_id, opendrive_lane_section_id_original, i,
                                                         opendrive_lane_id, lookup_table,
                                                         False)
                if row_number is not None:
                    return row_number

        # backward search first
        if opendrive_lane_section_id_original > opendrive_lane_section_id_search:
            for i in range(opendrive_lane_section_id_search - 1, -1, -1):
                # backward search
                row_number = lookup_table_search_section(opendrive_road_id, opendrive_lane_section_id_original, i,
                                                         opendrive_lane_id, lookup_table,
                                                         False)
                if row_number is not None:
                    return row_number
            for i in range(opendrive_lane_section_id_search + 1, max_lane_section + 1):
                # forward search
                row_number = lookup_table_search_section(opendrive_road_id, opendrive_lane_section_id_original, i,
                                                         opendrive_lane_id, lookup_table,
                                                         False)
                if row_number is not None:
                    return row_number

    return None


def lookup_table_search(opendrive_road_id, opendrive_lane_section_id, opendrive_lane_id, lookup_table, first_run):
    """
    look for VVM road id and VVM lane id that corresponds with the given opendrive road ,lane section and lane id
    if not found, search recursively in other lanesections of that road
    :param opendrive_road_id:
    :param opendrive_lane_section_id:
    :param opendrive_lane_id:
    :param lookup_table:
    :param first_run:
    :return: if found, the row number, if nothing was found - nothing is returned
    """
    counter = -1
    for row in lookup_table:
        counter += 1
        if row[0] == opendrive_road_id:
            if row[1] == opendrive_lane_section_id:
                if row[2] == opendrive_lane_id:
                    # found lane, return counter (row number)
                    return counter

    # if not found check if lane is in different lane section (work around solution, since not clear how to find out
    # beforehand in which road section lane is, check if road has different lane sections
    if first_run:
        max_lane_section = find_max_lane_section(opendrive_road_id, lookup_table)
        # run function for all found lane sections (forward and backward for beginning and end)
        for i in range(opendrive_lane_section_id + 1, max_lane_section + 1):
            # forward search
            row_number = lookup_table_search(opendrive_road_id, i, opendrive_lane_id, lookup_table, False)
            if row_number is not None:
                return row_number
        for i in range(opendrive_lane_section_id - 1, -1, -1):
            # backward search
            row_number = lookup_table_search(opendrive_road_id, i, opendrive_lane_id, lookup_table, False)
            if row_number is not None:
                return row_number

    return None


def find_max_lane_section(opendrive_road_id, lookup_table):
    """
    finds the maximum amount of lane sections for a certain road
    :param opendrive_road_id:
    :param lookup_table:
    :return:
    """
    max_lane_section = 0
    for row in lookup_table:
        if row[0] == opendrive_road_id:
            if row[1] > max_lane_section:
                max_lane_section = row[1]
    return max_lane_section


def find_corresponding_roads(junctions, id):
    """
    Creates a list of roads that a certain junction consists of.
    :param junctions: xml structure of all junctions.
    :param id: Junction id that is looked for
    :return:
    """
    white_list = []

    for junction in junctions:
        if junction.id == id:
            for connection in junction.connection:
                if connection.connecting_road not in white_list:
                    white_list.append(connection.connecting_road)
                if connection.incoming_road not in white_list:
                    white_list.append(connection.incoming_road)

    return white_list


def find_junction_xessor_roads(my_opendrive, whitelist):
    """
    Input is a list of roads, that the junction consists of. To complete the list of roads the junction consists of,
    the predecessors and successors of the allready identified roads are searched by looking through the roads link
    elements. Those are then added to the list and returned.
    :param my_opendrive: xml-structure of the opendrive file
    :param whitelist: List of roads that the junction consists of.
    :return:
    """
    white_list_static = whitelist.copy()    # non-changing list of the junctions road

    for road in my_opendrive.roads:
        if road.id in whitelist:
            # whenever a link element and entries exist, those will be appended
            if road.link:
                if road.link.successor:
                    # comparison is done to the initial list - so that the process will not bloat up itself
                    if road.link.successor.element_id not in white_list_static:
                        whitelist.append(road.link.successor.element_id)
                if road.link.predecessor:
                    if road.link.predecessor.element_id not in white_list_static:
                        whitelist.append(road.link.predecessor.element_id)

    return whitelist
