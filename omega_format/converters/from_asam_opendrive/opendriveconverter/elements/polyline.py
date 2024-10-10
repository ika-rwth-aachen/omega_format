import math
import numpy as np
from omega_format import Polyline
from ..logger import logger

def calculate_object_center_point(current_s, center_line_points, t=None, hdg=None, z_offset=None):
    if t is None:
        t = 0.0

    if hdg is None:
        hdg = 0.0

    if z_offset is None:
        z_offset = 0.0

    starting_point = np.array([0, 0, 0, 0, 0, 0])
    # get starting coordinates/values
    # center_line_points is a 6-dimensional list: [s, x, y, heading, z, superelevation]
    for l in range(0, len(center_line_points) - 1):
        if center_line_points[l, 0] <= current_s < center_line_points[l + 1, 0]:
            starting_point = center_line_points[l]
            break

    # Check if all necessary data has been taken
    if starting_point[1] == 0 and starting_point[2] == 0:
        logger.warning("Object's s-coordinate is beyond sections 's'-value. Is set to last known s-value.")
        starting_point = center_line_points[len(center_line_points) - 1]
    if not starting_point[4]:
        starting_point[4] = 0.0
    if not starting_point[5]:
        starting_point[5] = 0.0
    """
    The starting coordinates are those of corresponding roads center line!
    The object then has a vertical offset of t, towards the center line which in global coordinates is
    tilted by the roads heading angle here called hdg_s. t must also be corrected by the roads superelevation angle.
    So the objects center_point is the centerline coordinates + t_corrected * cos/sin (hdg_s + pi/2) because t is
    perpendicular to the roads s-direction.
    After finding the objects center coordinates the polyline must be calculated depending on the objects geometry.
    For further calculations the heading angle of the street and object are added onto another right away.
    """
    t_corrected = t * math.cos(starting_point[5])
    # in reference to the center_line_point [x, y, hdg, z]
    object_center_point = [starting_point[1] + t_corrected * math.cos(starting_point[3] + math.pi / 2),
                           starting_point[2] + t_corrected * math.sin(starting_point[3] + math.pi / 2),
                           starting_point[3] + hdg,
                           starting_point[4] + t_corrected * math.sin(starting_point[5]) + z_offset]

    return object_center_point


def calculate_polyline(center_line_points, object_center_point, length=None, width=None, radius=None, outlines=[], object_id=None):

    if object_center_point is None:
        # if there is no center point the object will be dropped
        return None

    if (object_center_point[0] or object_center_point[1] or object_center_point[2]) is None:
        # double check if an empty point is handed over - if empty the object will be dropped
        return None

    # Polyline calculations:
    if radius is not None:  # circular definition of the object
        polyline = get_polyline_from_radius(object_center_point, radius)

    elif (width and length) is not None:  # rectangular definition
        polyline = get_polyline_from_length_and_width(object_center_point, length=length, width=width)

    elif width is not None and length is None:  # signals only have a width dimension
        polyline = get_polyline_from_width(object_center_point, width)

    elif width is None and length is not None:  # some repeat objects like fences have no width
        polyline = get_polyline_from_length(object_center_point, length)

    elif outlines:
        polyline = get_polyline_from_outlines(center_line_points, object_center_point, outlines)

    else:
        # Backup if none of above worked, a point is returned
        polyline = get_polyline_from_point(object_center_point)
        logger.warning(f"Object {object_id} has no shape information. Assuming a point")

    check_polyline(polyline, length)

    return polyline


def get_polyline_from_outlines(center_line_points, center_point, outlines):

    for outline in outlines:
        """
        Multiple outlines are used to define e.g. a tree that has a narrow trunk and a wide crown. Our representation is
        not capable of such complexity, but we have to decide which outline to use. Ideally we would choose the one
        on the streets elevation level. For the cornerRoad geometry this should always be the case.
        For the cornerLocal geometry there might be divergency.
        """
        geometry = outline.outline_geometry
        # It seems only one sort (road/local) is used at a time
        if geometry.corner_local:
            points = len(geometry.corner_local)
            pos_x = np.zeros(points)
            pos_y = np.zeros(points)
            pos_z = np.zeros(points)
            # CornerLocal geometry is defined by u,v,z which are relative to the already calculated center_point
            for i, corner_local in enumerate(geometry.corner_local):
                # the vector of the u,v coordinates in combination with center_points hdg angle leads to its absolute pos
                vector = math.sqrt(corner_local.u ** 2 + corner_local.v ** 2)
                hdg_total = math.atan2(corner_local.v, corner_local.u) + center_point[2]
                # actual coordinates:
                pos_x[i] = center_point[0] + vector * math.cos(hdg_total)
                pos_y[i] = center_point[1] + vector * math.sin(hdg_total)
                pos_z[i] = center_point[3] + corner_local.z

        elif geometry.corner_road:
            points = len(geometry.corner_road)
            pos_x = np.zeros(points)
            pos_y = np.zeros(points)
            pos_z = np.zeros(points)
            # CornerRoad is defined by s,t which means a relative position to the street center - calculation exists
            for i, corner_road in enumerate(geometry.corner_road):
                corner_road_point = calculate_object_center_point(corner_road.s, center_line_points, corner_road.t)
                # actual coordinates
                pos_x[i] = corner_road_point[0]
                pos_y[i] = corner_road_point[1]
                pos_z[i] = corner_road_point[3]
        else:
            # Backup strategy if no outline geometry is given - return single point
            return get_polyline_from_point(center_point)

    return Polyline(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)


def get_polyline_from_point(center_point):
    """
    Creates a polyline from a signals center point coordinates.
    :param center_point: Center point.
    :return: Polyline of one coordinate point.
    """
    pos_x = np.zeros(1)
    pos_y = np.zeros(1)
    pos_z = np.zeros(1)
    pos_x[0] = center_point[0]
    pos_y[0] = center_point[1]
    pos_z[0] = center_point[3]

    return Polyline(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)


def get_polyline_from_width(center_point, width):
    """
    Creates a polyline from a signals center point coordinates and width.
    :param center_point: Signals center point.
    :param width: Width of the signal.
    :return: Polyline of two coordinates.
    """
    pos_x = np.zeros(2)
    pos_y = np.zeros(2)
    pos_z = np.zeros(2)
    pos_x[0] = center_point[0] - width / 2 * math.sin(center_point[2])
    pos_y[0] = center_point[1] + width / 2 * math.cos(center_point[2])
    pos_z[0] = center_point[3]
    pos_x[1] = center_point[0] + width / 2 * math.sin(center_point[2])
    pos_y[1] = center_point[1] - width / 2 * math.cos(center_point[2])
    pos_z[1] = center_point[3]

    return Polyline(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)


def get_polyline_from_length(center_point, length):
    """
    Creates a polyline from a objects center point coordinates and length.
    :param center_point: Objects center point.
    :param length: Length of the object.
    :return: Polyline of two coordinates.
    """
    pos_x = np.zeros(2)
    pos_y = np.zeros(2)
    pos_z = np.zeros(2)
    pos_x[0] = center_point[0] + length / 2 * math.cos(center_point[2])
    pos_y[0] = center_point[1] + length / 2 * math.sin(center_point[2])
    pos_z[0] = center_point[3]
    pos_x[1] = center_point[0] - length / 2 * math.cos(center_point[2])
    pos_y[1] = center_point[1] - length / 2 * math.sin(center_point[2])
    pos_z[1] = center_point[3]

    return Polyline(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)


def get_polyline_from_length_and_width(center_point, length, width):
    """
    :param center_point: Objects center point.
    :param length: Objects length.
    :param width: Objects width.
    :return: Returns a polyline with 4 points to describe a rectangular object.
    """
    pos_x = np.zeros(4)
    pos_y = np.zeros(4)
    pos_z = np.zeros(4)

    pos_x[0] = center_point[0] + length / 2 * math.cos(center_point[2]) - width / 2 * math.sin(center_point[2])
    pos_y[0] = center_point[1] + length / 2 * math.sin(center_point[2]) + width / 2 * math.cos(center_point[2])
    pos_z[0] = center_point[3]
    pos_x[1] = center_point[0] - length / 2 * math.cos(center_point[2]) - width / 2 * math.sin(center_point[2])
    pos_y[1] = center_point[1] - length / 2 * math.sin(center_point[2]) + width / 2 * math.cos(center_point[2])
    pos_z[1] = center_point[3]
    pos_x[2] = center_point[0] - length / 2 * math.cos(center_point[2]) + width / 2 * math.sin(center_point[2])
    pos_y[2] = center_point[1] - length / 2 * math.sin(center_point[2]) - width / 2 * math.cos(center_point[2])
    pos_z[2] = center_point[3]
    pos_x[3] = center_point[0] + length / 2 * math.cos(center_point[2]) + width / 2 * math.sin(center_point[2])
    pos_y[3] = center_point[1] + length / 2 * math.sin(center_point[2]) - width / 2 * math.cos(center_point[2])
    pos_z[3] = center_point[3]

    return Polyline(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)


def get_polyline_from_radius(center_point, radius, resolution=None):
    """
    Converts a circular object into a finite number of coordinate pairs represented in a polyline.
    :param center_point: Center of the circle
    :param radius: Radius of the circle
    :param resolution: Finite number, by how many coordinate pairs the circle should be represented by
    :return: Polyline
    """
    if resolution is None:
        resolution = 8
    pos_x = np.zeros(resolution)
    pos_y = np.zeros(resolution)
    pos_z = np.zeros(resolution)
    for i in range(resolution):
        pos_x[i] = center_point[0] + radius * math.cos((i / resolution) * 2 * math.pi)
        pos_y[i] = center_point[1] + radius * math.sin((i / resolution) * 2 * math.pi)
        pos_z[i] = center_point[3]

    return Polyline(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)


def get_polyline_for_rect_obj_repeat(point_start, point_end, width_start, width_end):
    """
    :param center_point: Objects center point.
    :param length: Objects length.
    :param width: Objects width.
    :return: Returns a polyline with 4 points to describe a rectangular object.
    """
    pos_x = np.zeros(4)
    pos_y = np.zeros(4)
    pos_z = np.zeros(4)

    pos_x[0] = point_start[0] - width_start / 2 * math.sin(point_start[2])
    pos_y[0] = point_start[1] + width_start / 2 * math.cos(point_start[2])
    pos_z[0] = point_start[3]
    pos_x[1] = point_start[0] - width_start / 2 * math.sin(point_start[2])
    pos_y[1] = point_start[1] + width_start / 2 * math.cos(point_start[2])
    pos_z[1] = point_start[3]
    pos_x[2] = point_end[0] + width_end / 2 * math.sin(point_end[2])
    pos_y[2] = point_end[1] - width_end / 2 * math.cos(point_end[2])
    pos_z[2] = point_end[3]
    pos_x[3] = point_end[0] + width_end / 2 * math.sin(point_end[2])
    pos_y[3] = point_end[1] - width_end / 2 * math.cos(point_end[2])
    pos_z[3] = point_end[3]

    return Polyline(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)


def create_polyline_from_list(polyline_list, dimension):
    shape = int(dimension * len(polyline_list))
    pos_x = np.zeros(shape)
    pos_y = np.zeros(shape)
    pos_z = np.zeros(shape)

    if dimension == 1:
        for i in range(0, shape):
            pos_x[i] = polyline_list[i].pos_x[0]
            pos_y[i] = polyline_list[i].pos_y[0]
            pos_z[i] = polyline_list[i].pos_z[0]
    else:
        for i in range(0, len(polyline_list)):
            pos_x[i] = polyline_list[i].pos_x[0]
            pos_y[i] = polyline_list[i].pos_y[0]
            pos_z[i] = polyline_list[i].pos_z[0]

            pos_x[shape - 1 - i] = polyline_list[i].pos_x[1]
            pos_y[shape - 1 - i] = polyline_list[i].pos_y[1]
            pos_z[shape - 1 - i] = polyline_list[i].pos_z[1]

    return Polyline(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)


def sum_two_polylines(polyline_1, polyline_2):
    # to make the polyline continuous one polyline must be flipped
    pos_x_new = np.concatenate((polyline_1.pos_x, np.flip(polyline_2.pos_x)), 0)
    pos_y_new = np.concatenate((polyline_1.pos_y, np.flip(polyline_2.pos_y)), 0)
    pos_z_new = np.concatenate((polyline_1.pos_z, np.flip(polyline_2.pos_z)), 0)
    return Polyline(pos_x=pos_x_new, pos_y=pos_y_new, pos_z=pos_z_new)


def get_outlines_max_height(outlines):
    height = []
    for outline in outlines:
        geometry = outline.outline_geometry

        if geometry.corner_local:
            for corner_local in geometry.corner_local:
                if corner_local.height is not None:
                    height.append(corner_local.height)

        elif geometry.corner_road:
            for corner_road in geometry.corner_road:
                if corner_road.height is not None:
                    height.append(corner_road.height)

    if height:
        return max(height)
    else:
        return None


def check_polyline(polyline, length):
    """
    Calculates the distance between points of the polyline. Extremely high values will indicate a bad calculation.
    :param polyline:
    :return:
    """
    if not polyline:
        return
    value_list = np.linalg.norm(np.diff(np.stack([polyline.pos_x, polyline.pos_y]),axis=1),axis=0)

    if len(value_list)>0 and max(value_list) > 50.0:
        logger.warning(f'Squared distance of two points in one Polyline has a value of {max(value_list):.2f}. Value might be too high. ')
        #raise ValueError()
    return


def interpolate_linear(f0, f1, x0, x1, x):
    if f0 == "-":
        f0 = 0.0
        # if '-' means the value should be empty the interpolation is wrong
    if f1 == "-":
        f1 = 0.0
    f0 = float(f0)
    f1 = float(f1)
    result = f0 + ((f1 - f0) / (x1 - x0)) * (x - x0)
    return result
