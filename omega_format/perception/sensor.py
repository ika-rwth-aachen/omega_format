from pydantic import BaseModel
from pydantic.types import confloat
from pydantic import validator
from h5py import Group

from ..enums import PerceptionTypes
from ..pydantic_utils.pydantic_config import PydanticConfig


class Sensor(BaseModel):
    class Config(PydanticConfig):
        pass
    id: int = 0
    sensor_modality: PerceptionTypes.SensorModality = PerceptionTypes.SensorModality.LIDAR
    fusion_information: str = ""
    sensor_name: str = ""
    firmware_version: str = ""
    original_updaterate: float = 0.
    sensor_pos_longitudinal: float = 0.
    sensor_pos_lateral: float = 0.
    sensor_pos_z: float = 0.
    sensor_heading: float = 0.
    sensor_pitch: float = 0.
    sensor_roll: float = 0.

    max_range: confloat(ge=0) = 0.
    min_range: confloat(ge=0) = 0.
    fov_vertical: confloat(ge=0) = 0.
    fov_horizontal: confloat(ge=0) = 0.
    max_velocity: confloat(ge=0) = 0.
    min_velocity: float = 0.
    angle_resolution_vertical: confloat(ge=0) = 0.
    angle_resolution_horizontal: confloat(ge=0) = 0.
    range_resolution: confloat(ge=0) = 0.
    vertical_resolution: confloat(ge=0) = 0.
    velocity_resolution: confloat(ge=0) = 0.
    angle_accuracy: confloat(ge=0) = 0.
    vertical_accuracy: confloat(ge=0) = 0.
    range_accuracy: confloat(ge=0) = 0.
    velocity_accuracy: confloat(ge=0) = 0.
    angle_precision: confloat(ge=0) = 0.
    range_precision: confloat(ge=0) = 0.
    vertical_precision: confloat(ge=0) = 0.
    velocity_precision: confloat(ge=0) = 0.
    track_confirmation_latency: confloat(ge=0) = 0.
    track_drop_latency: confloat(ge=0) = 0.
    max_object_tracks: confloat(ge=0) = 0.

    @validator('sensor_heading', 'sensor_pitch', 'sensor_roll')
    def check_angle(cls, v):
        assert v.size==0 or -360 <= v <= 360, f'{v} is not a valid angle'
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        sub_group_name = group.name.rpartition('/')[-1]
        func = cls if validate else cls.construct
        self = func(
            id=int(sub_group_name),
            sensor_modality=PerceptionTypes.SensorModality(group.attrs['sensorModality']),
            fusion_information=group.attrs['fusionInformation'],
            sensor_name=group.attrs['sensorName'],
            firmware_version=group.attrs['firmwareVersion'],
            original_updaterate = group.attrs['originalUpdaterate'],
            sensor_pos_longitudinal=group.attrs['sensorPosLongitudinal'],
            sensor_pos_lateral=group.attrs['sensorPosLateral'],
            sensor_pos_z=group.attrs['sensorPosZ'],
            sensor_heading=group.attrs['sensorHeading'],
            sensor_pitch=group.attrs['sensorPitch'],
            sensor_roll=group.attrs['sensorRoll'],

            max_range=group.attrs['maxRange'],
            min_range=group.attrs['minRange'],
            fov_vertical=group.attrs['foVVertical'],
            fov_horizontal=group.attrs['foVHorizontal'],
            max_velocity=group.attrs['maxVelocity'],
            min_velocity=group.attrs['minVelocity'],
            angle_resolution_vertical=group.attrs['angleResolutionVertical'],
            angle_resolution_horizontal=group.attrs['angleResolutionHorizontal'],
            range_resolution=group.attrs['rangeResolution'],
            vertical_resolution=group.attrs['verticalResolution'],
            velocity_resolution=group.attrs['velocityResolution'],
            angle_accuracy=group.attrs['angleAccuracy'],
            vertical_accuracy=group.attrs['verticalAccuracy'],
            range_accuracy=group.attrs['rangeAccuracy'],
            velocity_accuracy=group.attrs['velocityAccuracy'],
            angle_precision=group.attrs['anglePrecision'],
            range_precision=group.attrs['rangePrecision'],
            vertical_precision=group.attrs['verticalPrecision'],
            velocity_precision=group.attrs['velocityPrecision'],
            track_confirmation_latency=group.attrs['trackConfirmationLatency'],
            track_drop_latency=group.attrs['trackDropLatency'],
            max_object_tracks=group.attrs['maxObjectTracks']
        )
        return self

    def to_hdf5(self, group: Group):
        group.attrs.create('sensorModality', data=self.sensor_modality)
        group.attrs.create('fusionInformation', data=self.fusion_information)
        group.attrs.create('sensorName', data=self.sensor_name)
        group.attrs.create('firmwareVersion', data=self.firmware_version)
        group.attrs.create('originalUpdaterate', data=self.original_updaterate)
        group.attrs.create('sensorPosLongitudinal', data=self.sensor_pos_longitudinal)
        group.attrs.create('sensorPosLateral', data=self.sensor_pos_lateral)
        group.attrs.create('sensorPosZ', data=self.sensor_pos_z)
        group.attrs.create('sensorHeading', data=self.sensor_heading)
        group.attrs.create('sensorPitch', data=self.sensor_pitch)
        group.attrs.create('sensorRoll', data=self.sensor_roll)

        group.attrs.create('maxRange', data=self.max_range)
        group.attrs.create('minRange', data=self.min_range)
        group.attrs.create('foVVertical', data=self.fov_vertical)
        group.attrs.create('foVHorizontal', data=self.fov_horizontal)
        group.attrs.create('maxVelocity', data=self.max_velocity)
        group.attrs.create('minVelocity', data=self.min_velocity)
        group.attrs.create('angleResolutionVertical', data=self.angle_resolution_vertical)
        group.attrs.create('angleResolutionHorizontal', data=self.angle_resolution_horizontal)
        group.attrs.create('rangeResolution', data=self.range_resolution)
        group.attrs.create('verticalResolution', data=self.vertical_resolution)
        group.attrs.create('velocityResolution', data=self.velocity_resolution)
        group.attrs.create('angleAccuracy', data=self.angle_accuracy)
        group.attrs.create('verticalAccuracy', data=self.vertical_accuracy)
        group.attrs.create('rangeAccuracy', data=self.range_accuracy)
        group.attrs.create('velocityAccuracy', data=self.velocity_accuracy)
        group.attrs.create('anglePrecision', data=self.angle_precision)
        group.attrs.create('rangePrecision', data=self.range_precision)
        group.attrs.create('verticalPrecision', data=self.vertical_precision)
        group.attrs.create('velocityPrecision', data=self.velocity_precision)
        group.attrs.create('trackConfirmationLatency', data=self.track_confirmation_latency)
        group.attrs.create('trackDropLatency', data=self.track_drop_latency)
        group.attrs.create('maxObjectTracks', data=self.max_object_tracks)
