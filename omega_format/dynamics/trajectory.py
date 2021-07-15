from pydantic import BaseModel, validator
from functools import cached_property
from typing import Optional
import numpy as np
from h5py import Group

from ..reference_resolving import raise_not_resolved
from ..pydantic_utils.pydantic_config import PydanticConfig


class Trajectory(BaseModel):
    class Config(PydanticConfig):
        pass
    pos_x: np.ndarray
    pos_y: np.ndarray
    pos_z: np.ndarray
    roll: np.ndarray
    pitch: np.ndarray
    heading: np.ndarray

    vel_longitudinal: Optional[np.ndarray]
    vel_lateral: Optional[np.ndarray]
    vel_z: Optional[np.ndarray]
    acc_longitudinal: Optional[np.ndarray]
    acc_lateral: Optional[np.ndarray]
    acc_z: Optional[np.ndarray]

    roll_der: Optional[np.ndarray]
    pitch_der: Optional[np.ndarray]
    heading_der: Optional[np.ndarray]

    @validator('*')  # the '*' means that this validator is applied to each member of Trajectory
    def check_array_length(cls, v, values):

        if not len(v) > 0:
            raise ValueError('received trajectory with empty array')

        if len(values) > 0:
            # first array would be validated if len(values)=0 -> no length to compare against
            # use the length of pos_x to check equality with other array length
            length = len(values.get('pos_x'))
            if len(v) != length:
                raise ValueError(f'length of all trajectory arrays must match, expected len {len(v)}, actual len {length}')
        return v

    @validator('vel_longitudinal', 'vel_lateral')
    def check_velocity(cls, v):
        for value in v:
            if value > 400*3.6:
                raise ValueError(f'velocity is over {400*3.6} m/s ({400} km/h)')
        return v

    @validator('acc_longitudinal', 'acc_lateral', 'acc_z')
    def check_acceleration(cls, v):
        for value in v:
            if value > 9.81*20:
                raise ValueError(f'acceleration over {9.81*20} m/s^2 ({20} g)')
        return v

    @validator('heading', 'roll', 'pitch')
    def check_angle(cls, v):
        for val in v:
            assert -360 <= val <= 360, f'{val} is not a valid angle'
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
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
        group.create_dataset('posX', data=self.pos_x)
        group.create_dataset('posY', data=self.pos_y)
        group.create_dataset('posZ', data=self.pos_z)
        group.create_dataset('roll', data=self.roll)
        group.create_dataset('pitch', data=self.pitch)
        group.create_dataset('heading', data=self.heading)
        group.create_dataset('velLongitudinal', data=self.vel_longitudinal)
        group.create_dataset('velLateral', data=self.vel_lateral)
        group.create_dataset('velZ', data=self.vel_z)
        group.create_dataset('accLateral', data=self.acc_lateral)
        group.create_dataset('accLongitudinal', data=self.acc_longitudinal)
        group.create_dataset('accZ', data=self.acc_z)
        group.create_dataset('rollDer', data=self.roll_der)
        group.create_dataset('pitchDer', data=self.pitch_der)
        group.create_dataset('headingDer', data=self.heading_der)

    @cached_property
    def vel(self):
        return np.sqrt(np.power(self.vel_lateral, 2) + np.power(self.vel_longitudinal, 2) + np.power(self.vel_z, 2))

    @cached_property
    def acc(self):
        return np.sqrt(np.power(self.acc_lateral, 2) + np.power(self.acc_longitudinal, 2) + np.power(self.acc_z, 2))

    @cached_property
    def is_still(self, vel_thresh=0.1, acc_thresh=0.1):
        return np.logical_and(self.vel <= vel_thresh, self.acc <= acc_thresh)

    @cached_property
    def is_static(self):
        return np.all(self.is_still)

    @cached_property
    def statistics(self):
        return tuple([tuple([np.min(o), np.max(o), np.mean(o), np.std(o)]) for o in [self.vel, self.acc]])

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        if i == input_recording.ego_id:
            return input_recording.ego_vehicle.tr
        else:
            return input_recording.road_users[i].tr
