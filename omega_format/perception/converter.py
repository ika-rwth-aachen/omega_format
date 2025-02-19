import os
import tempfile
from collections import UserDict
from copy import deepcopy
from json import load
from typing import Union
import shapely.geometry
import shapely.affinity
import h5py
import numpy as np
import pyproj
from ..dynamics import RoadUser
from ..reference_recording import ReferenceRecording
from ..perception_recording import PerceptionRecording
from ..enums import PerceptionTypes, ReferenceTypes
from .object import Object
from .sensor import Sensor
import importlib 


perc_format_ver = "1.3"
format_version = importlib.metadata.version('omega_format')

class Converter:
    perception_recording: PerceptionRecording
    reference_recording: ReferenceRecording
    ego_id: int
    ego_offset: float
    ego_obj: RoadUser
    converter_version: str
    config_dict: dict
    object_map: dict
    transformer: pyproj.Transformer
    sensor_config_dict: dict
    sensors: dict
    original_obj_id = dict
    sensor_list: list

    def __init__(self, reference_recording: ReferenceRecording, ego_id: int, ego_offset: float = None,
                 sensor_config_dict: dict = None, sensors: Union[dict, UserDict] = None, converter_version: str = None):
        self.reference_recording = reference_recording
        self.perception_recording = PerceptionRecording()
        self.ego_id = ego_id
        self.ego_offset = ego_offset
        self.ego_obj = self.reference_recording.ego_vehicle
        self.converter_version = converter_version
        self.original_obj_id = dict()

        self.transformer = pyproj.Transformer.from_crs(pyproj.CRS('EPSG:25832').geodetic_crs, pyproj.CRS('EPSG:25832'))

        with open(os.path.abspath(os.path.dirname(__file__)) + '/config.json', "r") as file:
            self.config_dict = load(file)
        # sensor information can be either provided from config or from parsed perception/sensor dictionary
        self.sensor_config_dict = sensor_config_dict
        self.sensors = sensors
        self.sensor_list = []

        reference_type = ReferenceTypes.RoadUserType
        perception_type = PerceptionTypes.ObjectClassification
        self.object_map = {
            reference_type.REGULAR: perception_type.CAR,
            reference_type.CAR: perception_type.CAR,
            reference_type.TRUCK: perception_type.TRUCK,
            reference_type.BUS: perception_type.TRUCK,
            reference_type.MOTORCYCLE: perception_type.MOTORCYCLE,
            reference_type.BICYCLE: perception_type.BICYCLE,
            reference_type.PEDESTRIAN: perception_type.PEDESTRIAN,
            reference_type.PUSHABLE_PULLABLE: perception_type.NO_INFO,
            reference_type.WHEELCHAIR: perception_type.SMALLER_THAN_CAR,
            reference_type.PERSONAL_MOBILITY_DEVICE: perception_type.SMALLER_THAN_CAR,
            reference_type.TRAILER: perception_type.BIGGER_THAN_CAR,
            reference_type.FARMING: perception_type.BIGGER_THAN_CAR,
            reference_type.RAIL: perception_type.BIGGER_THAN_CAR,
            reference_type.CARRIAGE: perception_type.BIGGER_THAN_CAR,
        }

    def convert_to_perception_format(self):
        self.add_meta_data()
        self.add_ego_position()
        self.add_meta_object()
        self.add_objects()
        self.add_sensors()
        self.filter_objects_outside_sensor_fov()
        return self.perception_recording, self.original_obj_id

    def add_meta_data(self):
        self.perception_recording.converter_version = self.converter_version if self.converter_version else self.config_dict['converterVersion']
        self.perception_recording.ego_offset = self.ego_offset if self.ego_offset else float(self.config_dict['egoOffset'])

        self.perception_recording.recorder_number = self.reference_recording.meta_data.recorder_number
        self.perception_recording.recording_number = self.reference_recording.meta_data.recording_number
        self.perception_recording.ego_id = self.ego_id
        self.perception_recording.timestamps = self.reference_recording.timestamps
        self.perception_recording.custom_information = 'artificially created sensor data'

    def add_ego_position(self):
        ego_length = self.ego_obj.end - self.ego_obj.birth + 1
        self.perception_recording.ego_position.heading.val = self.ego_obj.tr.heading
        self.perception_recording.ego_position.pos_latitude.val = np.empty(ego_length)
        self.perception_recording.ego_position.pos_longitude.val = np.empty(ego_length)

        for index in range(ego_length):
            ref_x, ref_y = self.transformer.transform(self.reference_recording.meta_data.reference_point_lat,
                                                      self.reference_recording.meta_data.reference_point_lon)

            ego_lat, ego_lon = self.transformer.transform(ref_x + self.ego_obj.tr.pos_x[index],
                                                          ref_y + self.ego_obj.tr.pos_y[index],
                                                          direction='INVERSE')

            self.perception_recording.ego_position.pos_latitude.val[index] = ego_lat
            self.perception_recording.ego_position.pos_longitude.val[index] = ego_lon

        # z information left empty

        # yaw rate and pitch left empty

        # dont set to zero --> leave empty
        '''
        variance_vec = np.full(ego_length, 0.0)
        self.perception_recording.ego_position.heading.var = variance_vec
        self.perception_recording.ego_position.pos_latitude.var = variance_vec
        self.perception_recording.ego_position.pos_longitude.var = variance_vec
        '''

    def add_meta_object(self):
        measured = PerceptionTypes.PerceptionType.MEASURED
        not_provided = PerceptionTypes.PerceptionType.NOT_PROVIDED
        determined = PerceptionTypes.PerceptionType.DETERMINED

        # first: set all attributes to measured
        for k, v in vars(self.perception_recording.meta_object).items():
            setattr(self.perception_recording.meta_object, k, measured)

        # second: set attributes that are not provided
        self.perception_recording.meta_object.dist_z_val_type = not_provided
        self.perception_recording.meta_object.dist_z_var_type = not_provided
        self.perception_recording.meta_object.rcs_val_type = not_provided
        self.perception_recording.meta_object.dist_longitudinal_var_type = not_provided
        self.perception_recording.meta_object.dist_lateral_var_type = not_provided
        self.perception_recording.meta_object.rel_vel_longitudinal_var_type = not_provided
        self.perception_recording.meta_object.rel_vel_lateral_var_type = not_provided
        self.perception_recording.meta_object.abs_vel_longitudinal_var_type = not_provided
        self.perception_recording.meta_object.abs_vel_lateral_var_type = not_provided
        self.perception_recording.meta_object.rel_acc_longitudinal_var_type = not_provided
        self.perception_recording.meta_object.rel_acc_lateral_var_type = not_provided
        self.perception_recording.meta_object.abs_acc_longitudinal_var_type = not_provided
        self.perception_recording.meta_object.abs_acc_lateral_var_type = not_provided
        self.perception_recording.meta_object.heading_var_type = not_provided
        self.perception_recording.meta_object.width_var_type = not_provided
        self.perception_recording.meta_object.height_var_type = not_provided
        self.perception_recording.meta_object.length_var_type = not_provided
        self.perception_recording.meta_object.height_val_type = not_provided
        self.perception_recording.meta_object.object_classification_confidence_val_type = not_provided
        self.perception_recording.meta_object.meas_state_val_type = not_provided

        # set attributes that are calculated from others
        self.perception_recording.meta_object.movement_classification_val_type = determined
        self.perception_recording.meta_object.rel_vel_longitudinal_val_type = determined
        self.perception_recording.meta_object.rel_vel_lateral_val_type = determined
        self.perception_recording.meta_object.rel_acc_longitudinal_val_type = determined
        self.perception_recording.meta_object.rel_acc_lateral_val_type = determined
        self.perception_recording.meta_object.age_val_type = determined


    def add_objects(self):
        for rid, road_user in self.reference_recording.road_users.items():
            if rid == self.ego_id:
                continue

            obj_birth_index = max(self.ego_obj.birth, road_user.birth)
            obj_death_index = min(self.ego_obj.end, road_user.end)
            if not road_user.in_timespan(obj_birth_index, obj_death_index):
                continue

            obj = self.create_object(road_user, obj_birth_index, obj_death_index)
            self.convert_absolute_to_relative_object_values(obj, obj_birth_index, obj_death_index)
            # self.fill_object_variances(obj)
            self.perception_recording.objects[rid] = obj

    def create_object(self, road_user: RoadUser, obj_birth_index: int, obj_death_index: int):
        obj = Object()
        obj_length = obj_death_index - obj_birth_index + 1

        self.fill_general_object_attributes(obj, obj_birth_index, obj_length, road_user)
        self.calculate_movement_classification(obj, obj_length, road_user)
        # self.calculate_object_azimuth(road_user, obj, obj_birth_index, obj_length)

        return obj

    def fill_general_object_attributes(self, obj, obj_birth_index, obj_length, road_user):
        obj.id = road_user.id
        obj.birth_stamp = obj_birth_index
        obj.object_classification.val = [self.object_map[ReferenceTypes.RoadUserType(road_user.type)]] * obj_length
        obj.object_classification.confidence = np.full(obj_length, 1.0)

        obj.heading.val = road_user.tr.heading
        obj.dist_lateral.val = road_user.tr.pos_x
        obj.dist_longitudinal.val = road_user.tr.pos_y
        obj.dist_z.val = road_user.tr.pos_z

        obj.abs_vel_longitudinal.val = road_user.tr.vel_longitudinal
        obj.abs_vel_lateral.val = road_user.tr.vel_lateral
        obj.abs_acc_longitudinal.val = road_user.tr.acc_longitudinal
        obj.abs_acc_lateral.val = road_user.tr.acc_lateral

        obj.width.val = np.full(obj_length, road_user.bb.width)
        obj.length.val = np.full(obj_length, road_user.bb.length)
        obj.height.val = np.full(obj_length, road_user.bb.height)

        obj.age = np.arange(0, obj_length, dtype=float)
        obj.confidence_of_existence = np.full(obj_length, 1.0)

        obj.tracking_point = [PerceptionTypes.TrackingPoint.CENTER_OF_VEHICLE] * obj_length
        obj.meas_state = [PerceptionTypes.MeasState.MEASURED] * obj_length

    def calculate_movement_classification(self, obj: Object, obj_length: int, road_user: RoadUser):
        if road_user.tr.is_static:
            obj.movement_classification = [PerceptionTypes.MovementClassification.STATIONARY] * obj_length
        else:
            obj.movement_classification = list(map(self.movement_mapper, list(road_user.tr.is_still)))

    @staticmethod
    def movement_mapper(is_still: bool):
        if is_still:
            return PerceptionTypes.MovementClassification.STOPPED
        else:
            return PerceptionTypes.MovementClassification.MOVING

    # not needed anymore
    '''
    def calculate_object_azimuth(self, road_user: RoadUser, obj: Object, obj_birth_index: int, obj_length: int):
        geod = pyproj.CRS.from_epsg(25832).get_geod()
        for index in range(obj_length):
            ego_lat = self.perception_recording.ego_position.pos_latitude.val[index + obj_birth_index - 1]
            ego_lon = self.perception_recording.ego_position.pos_longitude.val[index + obj_birth_index - 1]

            ego_x, ego_y = self.transformer.transform(ego_lat, ego_lon)
            obj_lat, obj_lon = self.transformer.transform(ego_x + road_user.tr.pos_x[index],
                                                          ego_y + road_user.tr.pos_y[index],
                                                          direction='INVERSE')

            azimuth1, azimuth2, distance = geod.inv(ego_lon, ego_lat, obj_lon, obj_lat)
            obj.azimuth.val = np.append(obj.azimuth.val, np.deg2rad(azimuth1))
    '''

    def convert_absolute_to_relative_object_values(self, obj: Object, obj_birth_index: int, obj_death_index: int):
        self.calculate_relative_distance(obj, obj_birth_index, obj_death_index)
        self.calculate_relative_velocity(obj, obj_birth_index, obj_death_index)
        self.calculate_relative_acceleration(obj, obj_birth_index, obj_death_index)

    def calculate_relative_distance(self, obj: Object, obj_birth_index: int, obj_death_index: int):
        # abs reference coordinate system -> relative perception coordinate system
        heading, dist_x, dist_y = self.transform_absolute_to_relative(
            ego_h=self.ego_obj.tr.heading[obj_birth_index:obj_death_index + 1],
            ego_x=self.ego_obj.tr.pos_x[obj_birth_index:obj_death_index + 1],
            ego_y=self.ego_obj.tr.pos_y[obj_birth_index:obj_death_index + 1],
            obj_h=obj.heading.val,
            obj_x=obj.dist_lateral.val,
            obj_y=obj.dist_longitudinal.val)
        obj.heading.val = heading
        obj.dist_lateral.val = dist_x + self.perception_recording.ego_offset
        obj.dist_longitudinal.val = dist_y

    def calculate_relative_velocity(self, obj: Object, obj_birth_index: int, obj_death_index: int):
        _, vel_x, vel_y = self.transform_absolute_to_relative(
            ego_h=self.ego_obj.tr.heading[obj_birth_index:obj_death_index + 1],
            ego_x=self.ego_obj.tr.vel_lateral[obj_birth_index:obj_death_index + 1],
            ego_y=self.ego_obj.tr.vel_longitudinal[obj_birth_index:obj_death_index + 1],
            obj_h=obj.heading.val,
            obj_x=obj.abs_vel_lateral.val,
            obj_y=obj.abs_vel_longitudinal.val)
        obj.rel_vel_lateral.val = vel_x
        obj.rel_vel_longitudinal.val = vel_y

    def calculate_relative_acceleration(self, obj: Object, obj_birth_index: int, obj_death_index: int):
        _, acc_x, acc_y = self.transform_absolute_to_relative(
            ego_h=self.ego_obj.tr.heading[obj_birth_index:obj_death_index + 1],
            ego_x=self.ego_obj.tr.acc_lateral[obj_birth_index:obj_death_index + 1],
            ego_y=self.ego_obj.tr.acc_longitudinal[obj_birth_index:obj_death_index + 1],
            obj_h=obj.heading.val,
            obj_x=obj.abs_acc_lateral.val,
            obj_y=obj.abs_acc_longitudinal.val)
        obj.rel_acc_lateral.val = acc_x
        obj.rel_acc_longitudinal.val = acc_y

    # not needed. The variances var type is set to not_provided
    '''
    def fill_object_variances(self, obj: Object):
        variance_vec = np.full(obj.len, 0.0)

        obj.dist_lateral.var = variance_vec
        obj.dist_longitudinal.var = variance_vec
        obj.dist_z.var = variance_vec
        obj.heading.var = variance_vec
        obj.azimuth.var = variance_vec

        obj.abs_vel_longitudinal.var = variance_vec
        obj.abs_vel_lateral.var = variance_vec
        obj.abs_acc_longitudinal.var = variance_vec
        obj.abs_acc_lateral.var = variance_vec

        obj.rel_vel_longitudinal.var = variance_vec
        obj.rel_vel_lateral.var = variance_vec
        obj.rel_acc_longitudinal.var = variance_vec
        obj.rel_acc_lateral.var = variance_vec

        obj.width.var = variance_vec
        obj.length.var = variance_vec
        obj.height.var = variance_vec

        obj.size2d.var = variance_vec
        obj.size3d.var = variance_vec

        obj.age.var = variance_vec
        obj.tracking_point.var = variance_vec
    '''

    def transform_absolute_to_relative(self, ego_h, ego_x, ego_y, obj_h, obj_x, obj_y):
        out_h = obj_h - ego_h
        for i in range(out_h.size):
            if out_h[i] < 0:
                out_h[i] += 360.

        x = obj_x - ego_x
        y = obj_y - ego_y
        heading = ego_h - 90.
        out_x = -np.multiply(x, np.cos(np.deg2rad(heading))) - np.multiply(y, np.sin(np.deg2rad(heading)))
        out_y = -np.multiply(x, np.sin(np.deg2rad(heading))) + np.multiply(y, np.cos(np.deg2rad(heading)))
        return out_h, out_x, out_y

    def add_sensors(self):
        if self.sensors is not None:
            for sensor_id, sensor in self.sensors.items():
                self.create_sensor_fov(sensor)
                self.perception_recording.sensors[sensor_id] = sensor
        elif self.sensor_config_dict is not None:
            for sensor_id, sensor_dict in enumerate(self.sensor_config_dict['sensors']):
                sensor = self.create_sensor_from_config(sensor_id, sensor_dict)
                self.create_sensor_fov(sensor)
                self.perception_recording.sensors[sensor_id] = sensor
        else:
            print("[ERROR] No sensor found!")
            exit(1)

    def create_sensor_from_config(self, sensor_id: int, sensor_dict: dict):
        temp = tempfile.TemporaryFile()
        with h5py.File(temp, 'w') as f:
            sensor_group = f.create_group(str(sensor_id))

            for key, value in sensor_dict.items():
                sensor_group.attrs.create(key, data=value)

            sensor = Sensor.from_hdf5(sensor_group)
            return sensor

    def create_sensor_fov(self, sensor: Sensor):
        ego_offset = self.perception_recording.ego_offset
        offset_x = sensor.sensor_pos_lateral
        offset_y = sensor.sensor_pos_longitudinal + ego_offset
        heading = sensor.sensor_heading
        dist_max = sensor.max_range
        fov_horizontal = sensor.fov_horizontal

        fov = shapely.affinity.translate(
                shapely.affinity.rotate(
                    shapely.geometry.Polygon([
                        [0,0],
                        np.array([np.cos(np.deg2rad(-fov_horizontal/2)), np.sin(np.deg2rad(-fov_horizontal/2))])*dist_max*2,
                        np.array([np.cos(np.deg2rad(fov_horizontal/2)), np.sin(np.deg2rad(fov_horizontal/2))])*dist_max*2
                    ]).intersection(
                        shapely.geometry.Point(0,0).buffer(dist_max)
                    ),
                    angle=heading+90, # positive == counter clockwise
                    origin=(0,0)
                ),
                xoff=offset_x+ego_offset,
                yoff=offset_y
            )
        self.sensor_list.append(fov)

    def filter_objects_outside_sensor_fov(self):
        for obj_index in list(self.perception_recording.objects.keys()):
            obj = self.perception_recording.objects[obj_index]
            obj_timespan_list = self.generate_object_in_ego_view_timespan_list(obj)
            self.cut_object_to_ego_fov(obj, obj_timespan_list)

    def generate_object_in_ego_view_timespan_list(self, obj: Object):
        obj_timespan_list = []
        start = -1

        for i in range(obj.len):
            x = obj.dist_lateral.val[i]
            y = obj.dist_longitudinal.val[i]
            l = obj.length.val[i]
            w = obj.width.val[i]
            heading = obj.heading.val[i]

            shape = shapely.affinity.rotate(
                shapely.geometry.Polygon([
                    (x-l/2,y-w/2),
                    (x+l/2,y-w/2),
                    (x+l/2,y+w/2),
                    (x-l/2,y+w/2)
                ]),
                angle=heading+90,
                origin='center'
            )

            if any([area.intersects(shape) for area in self.sensor_list]):
                if start == -1:
                    start = i
            elif start != -1:
                end = i - 1
                obj_timespan_list.append((start, end))
                start = -1
        if start != -1:
            end = obj.len - 1
            obj_timespan_list.append((start, end))
        return obj_timespan_list

    def cut_object_to_ego_fov(self, obj: Object, obj_timespan_list: list):
        if len(obj_timespan_list) == 0:
            del self.perception_recording.objects[obj.id]
        else:
            self.original_obj_id[obj.id] = obj.id
            copy_obj = deepcopy(obj)
            # first object appearance is set directly on the original object
            obj.cut_to_timespan(*obj_timespan_list[0])
            # further object appearance are set on a copy
            for start, end in obj_timespan_list[1:]:
                adj_obj = deepcopy(copy_obj)
                adj_obj.cut_to_timespan(start, end)
                adj_obj.id = f'RU{max([int(i[2:]) for i in self.perception_recording.objects.keys()]) + 1}'
                self.original_obj_id[adj_obj.id] = obj.id
                self.perception_recording.objects[adj_obj.id] = adj_obj