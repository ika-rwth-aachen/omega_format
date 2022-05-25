from pydantic.dataclasses import dataclass
from pydantic import validator, BaseModel
import numpy as np
from h5py import Group
from ..reference_resolving import InputClassBase


class Polyline(InputClassBase):
    pos_x: np.ndarray
    pos_y: np.ndarray
    pos_z: np.ndarray

    @validator('*')  # the '*' means that this validator is applied to each member of Trajectory
    def check_array_length(cls, v, values):
        if not len(v) > 0:
            raise ValueError('received trajectory with empty array')

        if len(values) > 0:
            # first array would be validated if len(values)=0 -> no length to compare against
            # use the length of pos_x to check equality with other array length
            length = len(values.get('pos_x'))
            if len(v) != length:
                raise ValueError(
                    f'length of all trajectory arrays must match, expected len {len(v)}, actual len {length}')
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = func(
            pos_x=group['posX'][:],
            pos_y=group['posY'][:],
            pos_z=group['posZ'][:]
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('posX', data=self.pos_x)
        group.create_dataset('posY', data=self.pos_y)
        group.create_dataset('posZ', data=self.pos_z)
