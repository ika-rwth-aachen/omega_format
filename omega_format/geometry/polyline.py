from pydantic import field_validator, model_validator
from h5py import Group
from ..reference_resolving import InputClassBase
from ..settings import get_settings
import pydantic_numpy.typing as pnd


class Polyline(InputClassBase):
    pos_x: pnd.NpNDArray
    pos_y: pnd.NpNDArray
    pos_z: pnd.NpNDArray

    @field_validator('*')
    @classmethod
    def check_array_length(cls, v):
        assert v.shape[0]>0, 'size zero polyline'
        return v
    
    @model_validator(mode='after')
    def check_same_length(self):
        assert self.pos_x.shape[0]==self.pos_y.shape[0]==self.pos_z.shape[0], 'Polyline has coordinates of different length'
        return self

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            pos_x=group['posX'][:],
            pos_y=group['posY'][:],
            pos_z=group['posZ'][:]
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('posX', data=self.pos_x, **get_settings().hdf5_compress_args)
        group.create_dataset('posY', data=self.pos_y, **get_settings().hdf5_compress_args)
        group.create_dataset('posZ', data=self.pos_z, **get_settings().hdf5_compress_args)
