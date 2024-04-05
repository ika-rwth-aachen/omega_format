from pydantic import field_validator, model_validator, Field
from typing import Optional
import numpy as np
from h5py import Group

from ..reference_resolving import raise_not_resolved, InputClassBase
from ..settings import get_settings
import pydantic_numpy.typing as pnd

class Trajectory(InputClassBase):
    pos_x: pnd.NpNDArray
    pos_y: pnd.NpNDArray
    pos_z: pnd.NpNDArray
    roll: pnd.NpNDArray 
    pitch: pnd.NpNDArray
    heading: pnd.NpNDArray

    vel_longitudinal: Optional[pnd.NpNDArray] = Field(default=None)
    vel_lateral: Optional[pnd.NpNDArray] = Field(default=None)
    vel_z: Optional[pnd.NpNDArray] = Field(default=None)
    acc_longitudinal: Optional[pnd.NpNDArray] = Field(default=None)
    acc_lateral: Optional[pnd.NpNDArray] = Field(default=None)
    acc_z: Optional[pnd.NpNDArray] = Field(default=None)

    roll_der: Optional[pnd.NpNDArray] = Field(default=None)
    pitch_der: Optional[pnd.NpNDArray] = Field(default=None)
    heading_der: Optional[pnd.NpNDArray] = Field(default=None)
    @model_validator(mode='after')
    def check_array_length(self):
        assert np.all(np.diff([v.shape[0] for v in self.model_dump().values() if v is not None])==0), 'all fields in Trajectory need to have the same length!'
        return self

    @field_validator('vel_longitudinal', 'vel_lateral')
    @classmethod
    def check_velocity(cls, v):
        for value in v:
            if value.size>0 and value > 400*3.6:
                raise ValueError(f'velocity is over {400*3.6} m/s ({400} km/h)')
        return v

    @field_validator('acc_longitudinal', 'acc_lateral', 'acc_z')
    @classmethod
    def check_acceleration(cls, v):
        if v.size>0 and np.any(v > 9.81*20):
            raise ValueError(f'acceleration over {9.81*20} m/s^2 ({20} g)')
        return v

    @field_validator('heading', 'roll', 'pitch')
    @classmethod
    def check_angle(cls, v):
        for val in v:
            assert val.size>0 and -360 <= val <= 360, f'{val} is not a valid angle'
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            pos_x=group["posX"][:],
            pos_y=group["posY"][:],
            pos_z=group["posZ"][:],
            roll=group["roll"][:],
            pitch=group["pitch"][:],
            heading=group["heading"][:],
            vel_longitudinal=group["velLongitudinal"][:],
            vel_lateral=group["velLateral"][:],
            vel_z=group["velZ"][:],
            acc_longitudinal=group["accLongitudinal"][:],
            acc_lateral=group["accLateral"][:],
            acc_z=group["accZ"][:],
            roll_der=group["rollDer"][:],
            pitch_der=group["pitchDer"][:],
            heading_der=group["headingDer"][:],
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('posX', data=self.pos_x, **get_settings().hdf5_compress_args)
        group.create_dataset('posY', data=self.pos_y, **get_settings().hdf5_compress_args)
        group.create_dataset('posZ', data=self.pos_z, **get_settings().hdf5_compress_args)
        group.create_dataset('roll', data=self.roll, **get_settings().hdf5_compress_args)
        group.create_dataset('pitch', data=self.pitch, **get_settings().hdf5_compress_args)
        group.create_dataset('heading', data=self.heading, **get_settings().hdf5_compress_args)
        group.create_dataset('velLongitudinal', data=self.vel_longitudinal, **get_settings().hdf5_compress_args)
        group.create_dataset('velLateral', data=self.vel_lateral, **get_settings().hdf5_compress_args)
        group.create_dataset('velZ', data=self.vel_z, **get_settings().hdf5_compress_args)
        group.create_dataset('accLateral', data=self.acc_lateral, **get_settings().hdf5_compress_args)
        group.create_dataset('accLongitudinal', data=self.acc_longitudinal, **get_settings().hdf5_compress_args)
        group.create_dataset('accZ', data=self.acc_z, **get_settings().hdf5_compress_args)
        group.create_dataset('rollDer', data=self.roll_der, **get_settings().hdf5_compress_args)
        group.create_dataset('pitchDer', data=self.pitch_der, **get_settings().hdf5_compress_args)
        group.create_dataset('headingDer', data=self.heading_der, **get_settings().hdf5_compress_args)

    @property
    def vel(self):
        if self.vel_lateral is None or self.vel_longitudinal is None:
            return None
        return np.sqrt(np.power(self.vel_lateral, 2) + np.power(self.vel_longitudinal, 2))# + np.power(self.vel_z, 2))

    @property
    def acc(self):
        if self.acc_lateral is None or self.acc_longitudinal is None:
            return None
        return np.sqrt(np.power(self.acc_lateral, 2) + np.power(self.acc_longitudinal, 2))# + np.power(self.acc_z, 2))

    @property
    def is_still(self, vel_thresh=0.1, acc_thresh=0.1):
        if self.vel is None or self.acc is None:
            return None
        return np.logical_and(self.vel <= vel_thresh, self.acc <= acc_thresh)

    @property
    def is_static(self):
        if self.is_still is None:
            return None
        return np.all(self.is_still)

    @property
    def statistics(self):
        return tuple([tuple([np.min(o), np.max(o), np.mean(o), np.std(o)]) for o in [self.vel, self.acc]])

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        if i == input_recording.ego_id:
            return input_recording.ego_vehicle.tr
        else:
            return input_recording.road_users[i].tr

    def __deepcopy__(self, memodict={}):
        return self.__class__(**self.model_dump())