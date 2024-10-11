# ruff: noqa: F405
from lxml import etree
from .elements import *  # noqa: F403
from ..opendriveconverter.logger import logger

def parse_opendrive(root_node):
    # Only accept xml element
    if not etree.iselement(root_node):
        raise TypeError("Argument rootNode is not a xml element")

    # generate openDrive element
    opendrive = OpenDrive()

    # Header
    header = root_node.find("header")
    if header is not None:
        parse_opendrive_header(opendrive, header)
    else:
        logger.warning("OpenDRIVE file needs to contain a header")

    # roads
    for road in root_node.findall("road"):
        parse_opendrive_road(opendrive, road)

    # junctions
    for junction in root_node.findall("junction"):
        parse_opendrive_junction(opendrive, junction)

    # junction group
    for junction_group in root_node.findall("junctionGroup"):
        parse_opendrive_junction_group(opendrive, junction_group)

    return opendrive


def parse_opendrive_header(opendrive, header):
    """parse header containing geo reference point"""

    parsed_header = Header()

    parsed_header.rev_major = header.get("revMajor")
    parsed_header.rev_minor = header.get("revMinor")
    parsed_header.name = header.get("name")
    parsed_header.version = header.get("version")
    parsed_header.date = header.get("date")
    parsed_header.north = header.get("north")
    parsed_header.south = header.get("south")
    parsed_header.west = header.get("west")
    parsed_header.vendor = header.get("vendor")

    # get geo reference point
    if header.find("geoReference") is not None:
        parsed_header.geo_reference = header.find("geoReference").text

    opendrive.header = parsed_header


def parse_opendrive_road(opendrive, opendrive_road):

    new_road = Road()

    # get top level information
    new_road.name = opendrive_road.get("name")
    new_road.length = float(opendrive_road.get("length"))
    new_road.id = int(opendrive_road.get("id"))
    new_road.junction = int(opendrive_road.get("junction"))
    new_road.rule = opendrive_road.get("rule")

    # parse for additional information in separate tags (link, elevation profile etc.)
    # Links
    opendrive_road_link = opendrive_road.find("link")
    if opendrive_road_link is not None:
        parse_opendrive_road_link(new_road, opendrive_road_link)
    # Type (can be 0 to n)
    opendrive_road_type = opendrive_road.find("type")
    if opendrive_road_type is not None:
        for opendrive_road_type in opendrive_road.findall("type"):
            parse_opendrive_road_type(new_road, opendrive_road_type)
    # PlanView
    opendrive_road_plan_view = opendrive_road.find("planView")
    if opendrive_road_plan_view is not None:
        parse_opendrive_road_plan_view(new_road, opendrive_road_plan_view)
    # ElevationProfile
    opendrive_road_elevation_profile = opendrive_road.find("elevationProfile")
    if opendrive_road_elevation_profile is not None:
        parse_opendrive_road_elevation_profile(new_road, opendrive_road_elevation_profile)
    # LateralProfile
    opendrive_road_lateral_profile = opendrive_road.find("lateralProfile")
    if opendrive_road_lateral_profile is not None:
        parse_opendrive_road_lateral_profile(new_road, opendrive_road_lateral_profile)
    # Lanes
    lanes = opendrive_road.find("lanes")

    if lanes is None:
        raise Exception("Road must have lanes element")

    # Lane offset
    for opendrive_lanes_lane_offset in lanes.findall("laneOffset"):
        parse_opendrive_road_lane_offset(new_road, opendrive_lanes_lane_offset)

    # Lane sections
    # lanes should contain at least one lane section
    for opendrive_lanes_lane_section in lanes.findall("laneSection"):
        parse_opendrive_road_lane_section(new_road, opendrive_lanes_lane_section)

    # surface
    opendrive_road_surface = opendrive_road.find("surface")
    if opendrive_road_surface is not None:
        parse_opendrive_road_surface(new_road, opendrive_road_surface)

    # objects
    opendrive_road_objects = opendrive_road.find("objects")
    if opendrive_road_objects is not None:
        parse_opendrive_road_objects(new_road, opendrive_road_objects)

    # signs
    opendrive_road_signals = opendrive_road.find("signals")
    if opendrive_road_signals is not None:
        parse_opendrive_road_signals(new_road, opendrive_road_signals)

    opendrive.roads.append(new_road)


def parse_opendrive_road_link(new_road, opendrive_road_link):

    predecessor = opendrive_road_link.find("predecessor")

    if predecessor is not None:
        new_road.link.predecessor = RoadLinkPredecessor(
            int(predecessor.get("elementId")),
            predecessor.get("elementType"),
            predecessor.get("contactPoint"),
            predecessor.get("elementDir"),
        )
        if predecessor.get("elementS"):
            new_road.link.predecessor.element_s = float(predecessor.get("elementS"))

    successor = opendrive_road_link.find("successor")

    if successor is not None:
        new_road.link.successor = RoadLinkSuccessor(
            int(successor.get("elementId")),
            successor.get("elementType"),
            successor.get("contactPoint"),
            successor.get("elementDir"),
        )
        if successor.get("elementS"):
            new_road.link.successor.element_s = float(successor.get("elementS"))


def parse_opendrive_road_type(new_road, opendrive_road_type):

    speed = None
    if opendrive_road_type.find("speed") is not None:

        speed = RoadTypeSpeed(
            speed_max = float(opendrive_road_type.find("speed").get("max")),
            unit=opendrive_road_type.find("speed").get("unit"),
        )

    parsed_road_type = RoadType(
        s = float(opendrive_road_type.get("s")),
        type = opendrive_road_type.get("type"),
        country = opendrive_road_type.get("country"),
        speed = speed
    )
    new_road.type.append(parsed_road_type)


def parse_opendrive_road_plan_view(new_road, opendrive_road_plan_view):
    #read geometry --> needs to be sampled later to transfor into polylines
    for geometry in opendrive_road_plan_view.findall("geometry"):
        new_geometry = RoadPlanViewGeometry()
        new_geometry.s = float(geometry.get("s"))
        new_geometry.x = float(geometry.get("x"))
        new_geometry.y = float(geometry.get("y"))
        new_geometry.hdg = float(geometry.get("hdg"))
        new_geometry.length = float(geometry.get("length"))
        #check for geometric element
        if geometry.find("line") is not None:
            new_geometry.line = RoadPlanViewGeometryLine(line=True)
        elif geometry.find("spiral") is not None:
            spiral = geometry.find("spiral")
            new_geometry.spiral = RoadPlanViewGeometrySpiral(
                curv_start = float(spiral.get("curvStart")),
                curv_end = float(spiral.get("curvEnd")),
            )
        elif geometry.find("arc") is not None:
            arc = geometry.find("arc")
            new_geometry.arc = RoadPlanViewGeometryArc(
                curvature=float(arc.get("curvature"))
            )
        elif geometry.find("poly3") is not None:
            poly3 = geometry.find("poly3")
            new_geometry.poly3 = RoadPlanViewGeometryPoly3(
                a=float(poly3.get("a")),
                b=float(poly3.get("b")),
                c=float(poly3.get("c")),
                d=float(poly3.get("d")),
            )
        elif geometry.find("paramPoly3") is not None:
            param_poly3 = geometry.find("paramPoly3")
            new_geometry.param_poly3 = RoadPlanViewGeometryParamPoly3(
                a_u=float(param_poly3.get("aU")),
                b_u=float(param_poly3.get("bU")),
                c_u=float(param_poly3.get("cU")),
                d_u=float(param_poly3.get("dU")),
                a_v=float(param_poly3.get("aV")),
                b_v=float(param_poly3.get("bV")),
                c_v=float(param_poly3.get("cV")),
                d_v=float(param_poly3.get("dV")),
                p_range=param_poly3.get("pRange")
            )
        #add query if none is persent?

        new_road.plan_view.geometry.append(new_geometry)


def parse_opendrive_road_elevation_profile(new_road, opendrive_road_elevation_profile):

    for elevation in opendrive_road_elevation_profile.findall("elevation"):
        new_elevation = RoadElevationProfileElevation(
            s = float(elevation.get("s")),
            a = float(elevation.get("a")),
            b = float(elevation.get("b")),
            c = float(elevation.get("c")),
            d = float(elevation.get("d")),
        )
        new_road.elevation_profile.elevations.append(new_elevation)


def parse_opendrive_road_lateral_profile(new_road, opendrive_road_lateral_profile):

    for superelevation in opendrive_road_lateral_profile.findall("superelevation"):
        new_superelevation = RoadLateralProfileSuperelevation(
            s=float(superelevation.get("s")),
            a=float(superelevation.get("a")),
            b=float(superelevation.get("b")),
            c=float(superelevation.get("c")),
            d=float(superelevation.get("d")),
        )
        new_road.lateral_profile.superelevations.append(new_superelevation)


def parse_opendrive_road_lane_offset(new_road, opendrive_lanes_lane_offset):
    new_lane_offset = RoadLanesLaneOffset(
        s=float(opendrive_lanes_lane_offset.get("s")),
        a=float(opendrive_lanes_lane_offset.get("a")),
        b=float(opendrive_lanes_lane_offset.get("b")),
        c=float(opendrive_lanes_lane_offset.get("c")),
        d=float(opendrive_lanes_lane_offset.get("d")),
    )
    new_road.lanes.lane_offset.append(new_lane_offset)


def parse_opendrive_road_lane_section(new_road, opendrive_lanes_lane_section):

    new_lane_section = RoadLanesLaneSection()
    new_lane_section.s = float(opendrive_lanes_lane_section.get("s"))
    new_lane_section.single_side = opendrive_lanes_lane_section.get("singleSide")

    # go through left, center and right section and get each lane and its properties
    sides = dict(
        left=new_lane_section.left_lanes,
        center=new_lane_section.center_lanes,
        right=new_lane_section.right_lanes,
    )

    for sideTag, newSideLanes in sides.items():
        side = opendrive_lanes_lane_section.find(sideTag)

        # check if lanes for side are present
        if side is None:
            continue

        for lane in side.findall("lane"):
            new_lane = RoadLanesLaneSectionLane()
            new_lane.id = int(lane.get("id"))
            new_lane.type = lane.get("type")
            # TODO check if required by specification
            new_lane.level = lane.get("level")

            # lane links (zero allowed and only one allowed)
            if lane.find("link") is not None:
                # find predecessors and successors (0...n allowed)
                new_lane_link = RoadLanesLaneSectionLaneLink()
                if lane.find("link").find("predecessor") is not None:
                    for predecessor in lane.find("link").findall("predecessor"):
                        new_lane_link.predecessor.append(int(predecessor.get("id")))
                if lane.find("link").find("successor") is not None:
                    for successor in lane.find("link").findall("successor"):
                        new_lane_link.successor.append(int(successor.get("id")))
                new_lane.link = new_lane_link

            # get material (zero to n allowed)
            if lane.find("material") is not None:
                for material in lane.findall("material"):
                    new_lane_material = RoadLanesLaneSectionLaneMaterial(
                        s_offset = float(material.get("sOffset")),
                        surface = material.get("surface"),
                        friction = material.get("friction"),
                        roughness = material.get("roughness"),
                    )
                    new_lane.material.append(new_lane_material)

            # get speed (zero no n allowed)
            if lane.find("speed") is not None:
                for speed in lane.findall("speed"):
                    new_lane_speed = RoadLanesLaneSectionLaneSpeed(
                        s_offset = float(speed.get("sOffset")),
                        max = speed.get("max"),
                        unit = speed.get("unit"),
                    )
                    new_lane.speed.append(new_lane_speed)

            # get access (zero to n allowed)
            if lane.find("access") is not None:
                for access in lane.findall("access"):
                    new_lane_access = RoadLanesLaneSectionLaneAccess(
                        s_offset = float(access.get("sOffset")),
                        rule = access.get("rule"),
                        restriction = access.get("restriction"),
                    )
                    new_lane.access.append(new_lane_access)

            # get road mark (zero to n allowed)
            if lane.find("roadMark") is not None:
                for road_mark in lane.findall("roadMark"):
                    new_lane_road_mark = RoadLanesLaneSectionLaneRoadMark(
                        s_offset = float(road_mark.get("sOffset")),
                        type = road_mark.get("type"),
                        weight = road_mark.get("weight"),
                        color = road_mark.get("color"),
                        material = road_mark.get("material"),
                        lane_change = road_mark.get("laneChange"),
                    )
                    if road_mark.get("height"):
                        new_lane_road_mark.height = float(road_mark.get("height"))
                    if road_mark.get("width"):
                        new_lane_road_mark.width = float(road_mark.get("width"))

                    new_lane.road_mark.append(new_lane_road_mark)

            # get rule (zero to n allowed)
            if lane.find("rule") is not None:
                for rule in lane.findall("rule"):
                    new_lane_rule = RoadLanesLaneSectionLaneRule(
                        s_offset = float(rule.get("sOffset")),
                        value = rule.get("value"),
                    )
                    new_lane.rule.append(new_lane_rule)

            # get width (zero to n allowed)
            if lane.find("width") is not None:
                for width in lane.findall("width"):
                    new_lane_width = RoadLanesLaneSectionLaneWidth(
                        s_offset = float(width.get("sOffset")),
                        a = float(width.get("a")),
                        b = float(width.get("b")),
                        c = float(width.get("c")),
                        d = float(width.get("d")),
                    )
                    new_lane.width.append(new_lane_width)

            # get height (zero to n possible)
            if lane.find("height") is not None:
                for height in lane.findall("height"):
                    if height.find("inner") is not None:
                        new_lane_height = RoadLanesLaneSectionLaneHeight(
                            s_offset = float(height.get("sOffset")),
                            inner = float(height.get("inner")),
                            outer = float(height.get("outer")),
                        )
                        new_lane.height.append(new_lane_height)

            # get borders (zero to n allowed)
            if lane.find("border") is not None:
                for border in lane.findall("border"):
                    new_lane_border = RoadLanesLaneSectionLaneBorder(
                        s_offset = float(border.get("sOffset")),
                        a = float(border.get("a")),
                        b = float(border.get("b")),
                        c = float(border.get("c")),
                        d = float(border.get("d")),
                    )
                    new_lane.border.append(new_lane_border)

            newSideLanes.append(new_lane)
    new_road.lanes.lane_section.append(new_lane_section)


def parse_opendrive_road_surface(new_road, opendrive_road_surface):
    if opendrive_road_surface.find("CRG") is not None:
        for surface_crg in opendrive_road_surface.findall("CRG"):
            new_road_surface_crg = RoadSurfaceCrg(
                file = surface_crg.get("file"),
                s_start = float(surface_crg.get("sStart")),
                s_end= float(surface_crg.get("sEnd")),
                orientation=surface_crg.get("orientation"),
                mode = surface_crg.get("mode"),
                purpose = surface_crg.get("purpose"),
                s_offset = float(surface_crg.get("sOffset")),
                t_offset=float(surface_crg.get("tOffset")),
                z_offset=float(surface_crg.get("zOffset")),
                z_scale=float(surface_crg.get("zScale")),
                h_offset=float(surface_crg.get("hOffset")),
            )
            new_road.surface.crg.append(new_road_surface_crg)


def parse_opendrive_road_objects(new_road, opendrive_road_objects):
    new_objects = RoadObjects()

    # Bridge
    road_objects_bridge = opendrive_road_objects.find("bridge")
    if road_objects_bridge is not None:
        for road_objects_bridge in opendrive_road_objects.findall("bridge"):
            parse_opendrive_road_objects_bridge(new_objects, road_objects_bridge)

    # Tunnel
    opendrive_road_objects_tunnel = opendrive_road_objects.find("tunnel")
    if opendrive_road_objects_tunnel is not None:
        for opendrive_road_objects_tunnel in opendrive_road_objects.findall("tunnel"):
            parse_opendrive_road_objects_tunnel(new_objects, opendrive_road_objects_tunnel)

    # Reference
    opendrive_road_objects_reference = opendrive_road_objects.find("reference")
    if opendrive_road_objects_reference is not None:
        for opendrive_road_objects_reference in opendrive_road_objects.findall("reference"):
            parse_opendrive_road_objects_reference(new_objects, opendrive_road_objects_reference)

    # Object
    opendrive_road_objects_object = opendrive_road_objects.find("object")
    if opendrive_road_objects_object is not None:
        for opendrive_road_objects_object in opendrive_road_objects.findall("object"):
            parse_opendrive_road_objects_object(new_objects, opendrive_road_objects_object)

    new_road.objects = new_objects


def parse_opendrive_object_lane_validity(road_object):
    validity_list = []
    validity = road_object.find("validity")
    if validity is not None:
        for validity in road_object.findall("validity"):
            new_object_validity = ObjectLaneValidity(
                from_lane=int(validity.get("fromLane")),
                to_lane=int(validity.get("toLane")),
            )
            validity_list.append(new_object_validity)
        return validity_list


def parse_opendrive_road_objects_tunnel(new_object, road_objects_tunnel):
    new_road_objects_tunnel = RoadObjectsTunnel(
        s = float(road_objects_tunnel.get("s")),
        length = float(road_objects_tunnel.get("length")),
        name = road_objects_tunnel.get("name"),
        id = int(road_objects_tunnel.get("id")),
        type = road_objects_tunnel.get("type"),
        lighting = road_objects_tunnel.get("lighting"),
        daylight = road_objects_tunnel.get("daylight"),
    )
    new_road_objects_tunnel.validity = parse_opendrive_object_lane_validity(road_objects_tunnel)
    new_object.tunnel.append(new_road_objects_tunnel)


def parse_opendrive_road_objects_bridge(new_object, road_objects_bridge):
    idx = road_objects_bridge.get('id')
    try: 
        idx = int(idx)
    except ValueError:
        new_idx = int('b0_r'.split('_')[0][1:])
        logger.warn(f'Cannot parse bridge id {idx}: interpreting as {new_idx}.')
        idx = new_idx

    new_road_objects_bridge = RoadObjectsBridge(
        s = float(road_objects_bridge.get("s")),
        length = float(road_objects_bridge.get("length")),
        name = road_objects_bridge.get("name"),
        id = idx,
        type=road_objects_bridge.get("type"),
    )
    new_road_objects_bridge.validity = parse_opendrive_object_lane_validity(road_objects_bridge)
    new_object.bridge.append(new_road_objects_bridge)


def parse_opendrive_road_objects_reference(new_object, road_objects_reference):
    new_road_objects_reference = RoadObjectsReference(
        s = float(road_objects_reference.get("s")),
        t = float(road_objects_reference.get("t")),
        id = int(road_objects_reference.get("id")),
        orientation = road_objects_reference.get("orientation"),
    )
    if road_objects_reference.get("zOffset"):
        new_road_objects_reference.z_offset = float(road_objects_reference.get("zOffset"))
    if road_objects_reference.get("validLength"):
        new_road_objects_reference.valid_length = float(road_objects_reference.get("validLength"))
    new_road_objects_reference.validity = parse_opendrive_object_lane_validity(road_objects_reference)
    new_object.object_reference.append(new_road_objects_reference)


def parse_opendrive_road_objects_object(new_object, road_objects_object):
    new_objects_object = RoadObjectsObject()
    new_objects_object.s = float(road_objects_object.get("s"))
    new_objects_object.t = float(road_objects_object.get("t"))
    if road_objects_object.get("zOffset"):
        new_objects_object.z_offset = float(road_objects_object.get("zOffset"))
    if road_objects_object.get("type"):
        if road_objects_object.get("type") != '-1':
            new_objects_object.type = road_objects_object.get("type")
        else:
            new_objects_object.type = 'UNKNOWN'
    else:
        new_objects_object.type = 'none'
    if road_objects_object.get("validLength"):
        new_objects_object.valid_length = float(road_objects_object.get("validLength"))
    new_objects_object.orientation = road_objects_object.get("orientation")
    new_objects_object.subtype = road_objects_object.get("subtype"),
    new_objects_object.dynamic = road_objects_object.get("dynamic"),
    if road_objects_object.get("hdg"):
        new_objects_object.hdg = float(road_objects_object.get("hdg"))
    new_objects_object.name = road_objects_object.get("name"),
    if road_objects_object.get("pitch"):
        new_objects_object.pitch = float(road_objects_object.get("pitch"))
    new_objects_object.id = int(road_objects_object.get("id")),
    if road_objects_object.get("roll"):
        new_objects_object.roll = float(road_objects_object.get("roll"))
    if road_objects_object.get("height"):
        new_objects_object.height = float(road_objects_object.get("height"))
    if road_objects_object.get("length"):
        new_objects_object.length = float(road_objects_object.get("length"))
    if road_objects_object.get("width"):
        new_objects_object.width = float(road_objects_object.get("width"))
    if road_objects_object.get("radius"):
        new_objects_object.radius = float(road_objects_object.get("radius"))

    # Material
    if road_objects_object.find("material") is not None:
        for material in road_objects_object.findall("material"):
            new_object_material = ObjectMaterial()
            new_object_material.surface=material.get("surface"),
            new_object_material.friction=material.get("friction"),
            new_object_material.roughness=material.get("roughness"),
            new_objects_object.material.append(new_object_material)

    # Repeat
    if road_objects_object.find("repeat") is not None:
        for repeat in road_objects_object.findall("repeat"):
            new_object_repeat = ObjectRepeat(
                s = float(repeat.get("s")),
                length = float(repeat.get("length")),
                distance = float(repeat.get("distance")),
                t_start = float(repeat.get("tStart")),
                t_end = float(repeat.get("tEnd")),
                height_start = float(repeat.get("heightStart")),
                height_end = float(repeat.get("heightEnd"))
            )
            if repeat.get("zOffsetStart"):
                new_object_repeat.z_offset_start = float(repeat.get("zOffsetStart"))
            if repeat.get("zOffsetEnd"):
                new_object_repeat.z_offset_end = float(repeat.get("zOffsetEnd"))
            if repeat.get("widthStart"):
                new_object_repeat.width_start = float(repeat.get("widthStart"))
            if repeat.get("widthEnd"):
                new_object_repeat.width_end = float(repeat.get("widthEnd"))
            if repeat.get("lengthStart"):
                new_object_repeat.length_start = float(repeat.get("lengthStart"))
            if  repeat.get("lengthEnd"):
                new_object_repeat.length_end = float(repeat.get("lengthEnd"))
            if repeat.get("radiusStart"):
                new_object_repeat.radius_start = float(repeat.get("radiusStart"))
            if repeat.get("radiusEnd"):
                new_object_repeat.radius_end = float(repeat.get("radiusEnd"))

            new_objects_object.repeat.append(new_object_repeat)

    # Parking Space
    if road_objects_object.find("parkingSpace") is not None:
        parking_space = road_objects_object.find("parkingSpace")
        new_parking_space = ObjectParkingSpace()
        new_objects_object.parking_space = new_parking_space

        if parking_space.get("access") is not None:
            new_objects_object.parking_space.access = parking_space.get("access")
        else:
            new_objects_object.parking_space.access = "all"
            """
            -"access" is an unnecessary information we do not process further, yet it is mandatory in OpenDrive, meaning
             that the object of type parkingSpace isn't defined in the correct way if missing. The value in this case
             is set to "all"
            -parkingSpace Objects are only closed with "parkingSpace/" but never initialized, also object type is set to
             "parking" instead of "parkingSpace"
            -self-closing elements are defined as empty elements --> they should be set to default values - is done here
             manually
            """
        if parking_space.get("restrictions") is not None:
            new_parking_space.restrictions = parking_space.get("restrictions")

    # outline - used twice
    def parse_outline(odr_outline):
        new_object_outline = ObjectOutline()
        if odr_outline.get("id"):
            new_object_outline.id = int(odr_outline.get("id"))
        new_object_outline.fill_type = odr_outline.get("fillType")
        new_object_outline.outer = odr_outline.get("outer")
        new_object_outline.lane_type = odr_outline.get("laneType")
        new_object_outline.outline_geometry = OutlineGeometry()

        for corner_road in odr_outline.findall("cornerRoad"):
            new_object_outline_geom_road = OutlineCornerRoad()
            new_object_outline_geom_road.dz = float(corner_road.get("dz"))
            new_object_outline_geom_road.height = float(corner_road.get("height"))
            if corner_road.get("id"):
                new_object_outline_geom_road.id = int(corner_road.get("id"))
            new_object_outline_geom_road.s = float(corner_road.get("s"))
            new_object_outline_geom_road.t = float(corner_road.get("t"))
            new_object_outline.outline_geometry.corner_road.append(new_object_outline_geom_road)

        for corner_local in odr_outline.findall("cornerLocal"):
            new_object_outline_geom_local = OutlineCornerLocal()
            new_object_outline_geom_local.height = float(corner_local.get("height", default=0))
            if corner_local.get("id"):
                new_object_outline_geom_local.id = int(corner_local.get("id"))
            new_object_outline_geom_local.u = float(corner_local.get("u"))
            new_object_outline_geom_local.v = float(corner_local.get("v"))
            new_object_outline_geom_local.z = float(corner_local.get("z"))
            new_object_outline.outline_geometry.corner_local.append(new_object_outline_geom_local)

        return new_object_outline

    # Outlines
    if road_objects_object.find("outlines") is not None:
        outlines = road_objects_object.find("outlines")
        new_object_outlines = ObjectOutlines()

        for outline in outlines.findall("outline"):
            new_object_outlines.objectOutlines.append(parse_outline(outlines))

        new_objects_object.outlines = new_object_outlines

    # Outline
    if road_objects_object.find("outline") is not None:
        outline = road_objects_object.find("outline")
        new_objects_object.outline = parse_outline(outline)

    # Validity
    new_objects_object.validity = parse_opendrive_object_lane_validity(road_objects_object)

    # Borders
    if road_objects_object.find("borders") is not None:
        borders = road_objects_object.find("borders")
        new_object_borders = ObjectBorders()
        # Border
        for border in borders.findall("border"):
            new_border = ObjectBorder(
                width = float(border.get("width")),
                type = border.get("type"),
                outline_id = int(border.get("outlineId"))
            )
            new_border.use_complete_outline = border.get("useCompleteOutline")

            # cornerReference
            if border.findall("cornerReference") is not None:
                for cornerReference in border.findall("cornerReference"):
                    new_corner_reference = MarkingCornerReference(
                        id = int(cornerReference.get("id"))
                    )
                    new_border.corner_reference.append(new_corner_reference)
            new_object_borders.borders.append(new_border)
        new_objects_object.borders = new_object_borders

    # Markings
    if road_objects_object.find("markings") is not None:
        object_markings = road_objects_object.find("markings")
        new_object_markings = ObjectMarkings()
        # Marking
        for marking in object_markings.findall("marking"):
            new_marking = ObjectMarking(
                side = marking.get("side"),
                weight = marking.get("weight"),
                color = marking.get("color"),
                space_length = float(marking.get("spaceLength")),
                line_length = float(marking.get("lineLength")),
                start_offset = float(marking.get("startOffset")),
                stop_offset = float(marking.get("stopOffset"))
            )
            if marking.get("width"):
                new_marking.width = float(marking.get("width"))
            if marking.get("zOffset"):
                new_marking.z_offset = float(marking.get("zOffset"))

            # cornerReference
            if marking.findall("cornerReference") is not None:
                for cornerReference in marking.findall("cornerReference"):
                    new_corner_reference = MarkingCornerReference(
                        id = int(cornerReference.get("id"))
                    )
                    new_marking.corner_reference.append(new_corner_reference)
            new_object_markings.marking.append(new_marking)
        new_objects_object.markings = new_object_markings

    new_object.object.append(new_objects_object)


def parse_opendrive_road_signals(new_road, opendrive_road_signals):
    new_signals = Signals()

    # signal
    opendrive_road_signals_signal = opendrive_road_signals.find("signal")
    if opendrive_road_signals_signal is not None:
        for opendrive_road_signals_signal in opendrive_road_signals.findall("signal"):
            parse_opendrive_road_signals_signal(new_signals, opendrive_road_signals_signal)

    # signalReference
    opendrive_road_signal_signal_reference = opendrive_road_signals.find("signalReference")
    if opendrive_road_signal_signal_reference is not None:
        for opendrive_road_signals_signal_reference in opendrive_road_signals.findall("signalReference"):
            parse_opendrive_road_signals_signal_reference(new_signals, opendrive_road_signals_signal_reference)

    new_road.signals = new_signals


def parse_opendrive_road_signals_signal(new_signals, opendrive_road_signals_signal):
    new_signal = Signal()
    new_signal.s = float(opendrive_road_signals_signal.get("s"))
    new_signal.t = float(opendrive_road_signals_signal.get("t"))
    new_signal.id = int(opendrive_road_signals_signal.get("id"))
    new_signal.name = opendrive_road_signals_signal.get("name")
    new_signal.dynamic = opendrive_road_signals_signal.get("dynamic")
    new_signal.orientation = opendrive_road_signals_signal.get("orientation")
    if opendrive_road_signals_signal.get("zOffset"):
        new_signal.z_offset = float(opendrive_road_signals_signal.get("zOffset"))
    new_signal.country = opendrive_road_signals_signal.get("country")
    new_signal.country_revision = opendrive_road_signals_signal.get("countryRevision")
    new_signal.type = opendrive_road_signals_signal.get("type")
    new_signal.subtype = opendrive_road_signals_signal.get("subtype")
    new_signal.value = opendrive_road_signals_signal.get("value")
    new_signal.unit = opendrive_road_signals_signal.get("unit")
    if opendrive_road_signals_signal.get("height"):
        new_signal.height = float(opendrive_road_signals_signal.get("height"))
    if opendrive_road_signals_signal.get("width"):
        new_signal.width = float(opendrive_road_signals_signal.get("width"))
    new_signal.text = opendrive_road_signals_signal.get("text")
    if opendrive_road_signals_signal.get("hOffset"):
        new_signal.h_offset = float(opendrive_road_signals_signal.get("hOffset"))
    if opendrive_road_signals_signal.get("pitch"):
        new_signal.pitch = float(opendrive_road_signals_signal.get("pitch"))
    if opendrive_road_signals_signal.get("roll"):
        new_signal.roll = float(opendrive_road_signals_signal.get("roll"))

    # physical Position
    if opendrive_road_signals_signal.find("physicalPosition"):
        new_physical_position = SignalPhysicalPosition()
        physical_position = opendrive_road_signals_signal.find("physicalPosition")

        # position Road
        if physical_position.find("positionRoad") is not None:
            position_road = physical_position.get("positionRoad")
            new_position_road = SignalPositionRoad()
            new_position_road.road_id = int(position_road.get("roadId"))
            new_position_road.s = float(position_road.get("s"))
            new_position_road.t = float(position_road.get("t"))
            new_position_road.z_offset = float(position_road.get("zOffset"))
            new_position_road.h_offset = float(position_road.get("hOffset"))
            if position_road.get("pitch"):
                new_position_road.pitch = float(position_road.get("pitch"))
            if position_road.get("roll"):
                new_position_road.roll = float(position_road.get("roll"))
            # add to physical position element
            new_physical_position.position_road = new_position_road

        # position Inertial
        if physical_position.find("positionInertial") is not None:
            position_inertial = physical_position.get("positionInertial")
            new_position_inertial = SignalPositionInertial()
            new_position_inertial.x = float(position_inertial.get("x"))
            new_position_inertial.y = float(position_inertial.get("y"))
            new_position_inertial.z = float(position_inertial.get("z"))
            new_position_inertial.hdg = float(position_inertial.get("hdg"))
            if position_inertial.get("pitch"):
                new_position_inertial.pitch = float(position_inertial.get("pitch"))
            if position_inertial.get("roll"):
                new_position_inertial.roll = float(position_inertial.get("roll"))
            # add to physical position element
            new_physical_position.position_inertial = new_position_inertial
        # add to new_signal
        new_signal.physical_position = new_physical_position

    # Validity
    new_signal.validity = parse_opendrive_object_lane_validity(opendrive_road_signals_signal)

    # Dependency
    if opendrive_road_signals_signal.find("dependency") is not None:
        for dependency in opendrive_road_signals_signal.findall("dependency"):
            new_dependency = SignalDependency()
            new_dependency.id = int(dependency.get("id"))
            new_dependency.type = dependency.get("type")

            new_signal.dependency = new_dependency

    # Reference
    if opendrive_road_signals_signal.find("reference") is not None:
        for reference in opendrive_road_signals_signal.findall("reference"):
            new_reference = SignalReference()
            new_reference.element_type = reference.get("elementType")
            new_reference.element_id = int(reference.get("elementId"))
            new_reference.type = reference.get("type")

            new_signal.reference = new_reference

    new_signals.signal.append(new_signal)


def parse_opendrive_road_signals_signal_reference(new_signals, opendrive_road_signals_signal_reference):
    new_signals_reference = SignalsReference(
        s=float(opendrive_road_signals_signal_reference.get("s")),
        t=float(opendrive_road_signals_signal_reference.get("t")),
        id=int(opendrive_road_signals_signal_reference.get("id")),
        orientation=opendrive_road_signals_signal_reference.get("orientation")
    )

    # Validity
    new_signals_reference.validity = parse_opendrive_object_lane_validity(opendrive_road_signals_signal_reference)

    new_signals.signal_reference.append(new_signals_reference)


def parse_opendrive_junction(opendrive, junction):
    new_junction = Junction()
    new_junction.id = int(junction.get("id"))
    new_junction.name = junction.get("name")
    new_junction.type = junction.get("type")
    if junction.get("sStart"):
        new_junction.s_start = float(junction.get("sStart"))
    if junction.get("sEnd"):
        new_junction.s_end = float(junction.get("sEnd"))

    # parse connection (one needs to be present, up to n allowed)
    for connection in junction.findall("connection"):
        new_connection = JunctionConnection()
        new_connection.id = int(connection.get("id"))
        new_connection.type = connection.get("type")
        new_connection.incoming_road = int(connection.get("incomingRoad"))
        new_connection.connecting_road = int(connection.get("connectingRoad"))
        new_connection.contact_point = connection.get("contactPoint")
        # predecessor allowed to be zero
        if connection.find("predecessor") is not None:
            predecessor = connection.get("predecessor")
            new_predecessor = JunctionPredecessor()
            new_predecessor.element_type = predecessor.get("elementType")
            new_predecessor.element_id = int(predecessor.get("elementId"))
            new_predecessor.element_s = float(predecessor.get("elementS"))
            new_predecessor.element_dir = predecessor.get("elementDir")
            new_connection.predecessor = new_predecessor
        # successor
        if connection.find("successor") is not None:
            successor = connection.get("successor")
            new_successor = JunctionPredecessor()
            new_successor.element_type = successor.get("elementType")
            new_successor.element_id = int(successor.get("elementId"))
            new_successor.element_s = float(successor.get("elementS"))
            new_successor.element_dir = successor.get("elementDir")
            new_connection.successor = new_successor

        # get link, allowed 0 to n
        if connection.find("laneLink") is not None:
            for laneLink in connection.findall("laneLink"):
                new_lane_link = JunctionLaneLink(int(laneLink.get("from")), int(laneLink.get("to")))
                new_connection.lane_link.append(new_lane_link)

        new_junction.connection.append(new_connection)

    # parse priority (0 to n allowed)
    if junction.find("priority") is not None:
        for priority in junction.findall("priority"):
            new_priority = JunctionPriority(high = priority.get("high"), low = priority.get("low"))

            new_junction.priority.append(new_priority)

    # parse controller (0 to n allowed)
    if junction.find("controller") is not None:
        for controller in junction.findall("controller"):
            new_controller = JunctionController(id = int(controller.get("id")))
            new_controller.type = controller.get("type")
            if controller.get("sequence"):
                new_controller.sequence = controller.get("sequence")

            new_junction.controller.append(new_controller)

    # parse surface (0 to 1 allowed)
    if junction.find("surface") is not None:
        surface = junction.get("surface")
        # crg zero to n allowd
        if surface.find("CRG") is not None:
            for crg in surface.findall("CRG"):
                surface_crg = crg.get("CRG")
                new_surface_crg = JunctionSurfaceCrg()
                new_surface_crg.file = surface_crg.get("file")
                new_surface_crg.mode = surface_crg.get("mode")
                new_surface_crg.purpose = surface_crg.get("purpose")
                if surface_crg.get("zOffset"):
                    new_surface_crg.z_offset = float(surface_crg.get("zOffset"))
                if surface_crg.get("zScale"):
                    new_surface_crg.z_scale = float(surface_crg.get("zScale"))
                new_junction.surface.crg.append(new_surface_crg)

    opendrive.junctions.append(new_junction)


def parse_opendrive_junction_group(opendrive, junction_group):
    new_junction_group = JunctionGroup()
    new_junction_group.id = int(junction_group.get("id"))
    new_junction_group.name = junction_group.get("name")
    new_junction_group.type = junction_group.get("type")

    for junction_reference in junction_group.findall("junctionReference"):
        new_junction_reference = JunctionReference()
        new_junction_reference.junction = int(junction_reference.get("junction"))
        new_junction_group.junction_reference.append(new_junction_reference)

    opendrive.junction_group.append(new_junction_group)
