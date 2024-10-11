import numpy as np
import copy
from ..logger import logger

from omega_format.converters.from_asam_opendrive.eulerspiral import EulerSpiral


def calculate_s_index(center_line_points, s_value):
    """
    Returns the index in center_line_points of an input s-value
    :param center_line_points:
    :param s_value:
    :return: Index of point in
    """
    return np.argwhere(center_line_points[:,0] - s_value>=0)[0][0]
    


def get_center_line_points(road, step_size):
    """
    get plan view geometries and transfer into points
    :param road:
    :param step_size:
    :return: center_line_points
    """
    # run over all geometry elements

    center_line_points = []
    deltas = []
    for i, geometry_entry in enumerate(road.plan_view.geometry):
        ps, d = sample_points(geometry_entry, step_size)
        center_line_points.append(ps)
        deltas.append(d)
    for i in range(1,len(deltas)):
        deltas[i] = deltas[i-1][-1]+deltas[i]
    n_coordinates_per_segment = [x.shape[1] for x in center_line_points]
    center_line_points_xy = np.concatenate(center_line_points, axis=1).T
    delta_ss = np.concatenate(deltas)
    center_line_points = np.zeros([len(center_line_points_xy), 6])
    center_line_points[:,1:4] = center_line_points_xy
    center_line_points[:,0] = delta_ss
    # remove duplicates (because each segment produces 0 to length)
    center_line_points = center_line_points[~np.concatenate([np.diff(delta_ss)==0, [False]]), :]
    
    if road.elevation_profile.elevations:
        for i, elevations in enumerate(road.elevation_profile.elevations):
            delta_s = center_line_points[:,0]
            idxs = delta_s>=elevations.s
            if i < len(road.elevation_profile.elevations)-1:
                idxs = np.logical_and(idxs, delta_s < road.elevation_profile.elevations[i+1].s)
            delta_s = delta_s[idxs] - elevations.s
            center_line_points[idxs, 4] = elevations.a + elevations.b * delta_s + \
                                elevations.c * np.power(delta_s, 2) + elevations.d * np.power(delta_s, 3)
    if road.lateral_profile.superelevations:
        for i, supelev in enumerate(road.lateral_profile.superelevations):
            delta_s = center_line_points[:,0]
            idxs = delta_s>=supelev.s
            if i < len(road.lateral_profile.superelevations)-1:
                idxs = np.logical_and(idxs, delta_s < road.lateral_profile.superelevations[i+1].s)
            delta_s = delta_s[idxs] - supelev.s
            # get angle in rad
            center_line_points[idxs, 5] = supelev.a + supelev.b * delta_s + supelev.c * np.power(
                delta_s, 2) + supelev.d * np.power(delta_s, 3)

    # make copy of center_line_points for objects and signals where lane offset is not considered
    #plt.figure();plt.plot(center_line_points[:, 0], center_line_points[:, 1]);plt.savefig('test.png')
    clp_no_offset = copy.copy(center_line_points)

    # move center line by lane offset(s)
    for i, lane_offset in enumerate(road.lanes.lane_offset):
        delta_s = center_line_points[:,0]
        idxs = delta_s>=lane_offset.s
        if i < len(road.lanes.lane_offset)-1:
            idxs = np.logical_and(idxs, delta_s < road.lanes.lane_offset[i+1].s)
        delta_s = delta_s[idxs] - lane_offset.s
        # calculate current offset
        lane_offset_value = lane_offset.a + lane_offset.b * delta_s + lane_offset.c * np.power(delta_s, 2) + lane_offset.d * np.power(delta_s, 3)
        # add offset to center line points
        center_line_points[idxs, 1] = center_line_points[idxs, 1] + lane_offset_value * np.cos(center_line_points[idxs, 3]+ np.pi / 2)
        center_line_points[idxs, 2] = center_line_points[idxs, 2] + lane_offset_value * np.sin(center_line_points[idxs, 3]+ np.pi / 2)
        # add superelevation to z coordinate
        center_line_points[idxs, 4] = center_line_points[idxs, 4] + np.sin(center_line_points[idxs, 5]) * lane_offset_value

    # todo remove once failure found
    #plt.plot(center_line_points[:, 1], center_line_points[:, 2])
    #plt.show()

    return center_line_points, clp_no_offset, n_coordinates_per_segment



def sample_points(geometry_entry, step_size):
    # get distance from start point of geometry segment
    delta_s = np.arange(0, #geometry_entry.s, 
                        geometry_entry.length, # + geometry_entry.s
                        step_size)
    if delta_s[-1]<geometry_entry.length:
        delta_s = np.concatenate([delta_s, [geometry_entry.length]])
    # check which geometry type
    if geometry_entry.line.line is not None:
        # calculate x and y for line
        #https://github.com/pageldev/libOpenDRIVE/blob/master/src/Geometries/Line.cpp#L14
        center_line_points = np.stack([
            geometry_entry.x + delta_s * np.cos(geometry_entry.hdg),
            geometry_entry.y + delta_s * np.sin(geometry_entry.hdg),
            np.ones_like(delta_s)*geometry_entry.hdg
        ])

    elif geometry_entry.arc.curvature is not None:
        #delta_s /= geometry_entry.length
        # https://github.com/pageldev/libOpenDRIVE/blob/master/src/Geometries/Arc.cpp#L15
        r = 1 / geometry_entry.arc.curvature
        angle_at_s = delta_s * geometry_entry.arc.curvature - np.pi / 2
        xs = r * (np.cos(geometry_entry.hdg + angle_at_s) - np.sin(geometry_entry.hdg)) + geometry_entry.x
        ys = r * (np.sin(geometry_entry.hdg + angle_at_s) + np.cos(geometry_entry.hdg)) + geometry_entry.y
        delta_phi = delta_s / r
        center_line_points = np.stack([
            xs,
            ys,
            geometry_entry.hdg + delta_phi
        ])
        #delta_s *= geometry_entry.length

    elif geometry_entry.spiral.curv_end is not None:
        # normalize curvature to geometry length, as it increases linear along its length from start to end

        spiral = EulerSpiral.createFromLengthAndCurvature(geometry_entry.length, geometry_entry.spiral.curv_start, geometry_entry.spiral.curv_end)

        
        center_line_points = np.stack(spiral.calc(delta_s, geometry_entry.x, geometry_entry.y, geometry_entry.spiral.curv_start, geometry_entry.hdg))

    elif geometry_entry.poly3.a is not None:
        logger.info("cubic polynom is outdated in OpenDrive Format v.1.6.1, it might not work correctly")
        u = delta_s
        v = geometry_entry.poly3.a + geometry_entry.poly3.b * u + geometry_entry.poly3.c * u ** 2 \
            + geometry_entry.poly3.d * u ** 3
        rotation_total = np.atan2(v, u) + geometry_entry.hdg

        center_line_points = np.stack([
            geometry_entry.x + np.sqrt(u ** 2 + v ** 2) * np.cos(rotation_total),
            geometry_entry.y + np.sqrt(u ** 2 + v ** 2) * np.sin(rotation_total),
            rotation_total
        ])

    elif geometry_entry.param_poly3.a_u is not None:
        if geometry_entry.param_poly3.p_range == "arcLength":
            p = delta_s
            if p > geometry_entry.length:
                p = geometry_entry.length
        else:  # Normalized to geometry_entry.length is the usual case
            p = delta_s / geometry_entry.length
            p = np.clip(p, 0, 1)

        def calculate_u_v(p, param_poly3):
            # Calculation of u, v - coordinates of the local coordinate-system
            u = param_poly3.a_u + param_poly3.b_u * p + param_poly3.c_u * (p ** 2) + param_poly3.d_u * (p ** 3)
            v = param_poly3.a_v + param_poly3.b_v * p + param_poly3.c_v * (p ** 2) + param_poly3.d_v * (p ** 3)
            return u, v

        # Calculation of u, v - coordinates of the local coordinate-system
        u, v = calculate_u_v(p, geometry_entry.param_poly3)
        # calculation of a point slightly ahead, to get the gradient of the cubic curve for the heading angle
        u_1, v_1 = calculate_u_v(p + 0.00001, geometry_entry.param_poly3)

        # heading angle in total is the gradient of the cubic curve (in local sys) + heading angle of the local system
        hdg_total = np.atan2(v_1 - v, u_1 - u) + geometry_entry.hdg

        # transform back to global coordinates:
        origin_offset = np.sqrt(geometry_entry.param_poly3.a_v ** 2 + geometry_entry.param_poly3.a_u ** 2)
        origin_offset_hdg = np.atan2(geometry_entry.param_poly3.a_v, geometry_entry.param_poly3.a_u)
        rotation_total = geometry_entry.hdg + np.atan2(v, u)

        center_line_points = np.stack([
            geometry_entry.x + np.sqrt(u ** 2 + v ** 2) * np.cos(rotation_total) - \
                                   origin_offset * np.cos(origin_offset_hdg),
            geometry_entry.y + np.sqrt(u ** 2 + v ** 2) * np.sin(rotation_total) - \
                                   origin_offset * np.sin(origin_offset_hdg),
            hdg_total
        ])
        if geometry_entry.param_poly3.p_range != "arcLength":
            delta_s *= geometry_entry.length
    else:
        logger.warning("Centerline geometry type unknown!")

    return center_line_points, delta_s