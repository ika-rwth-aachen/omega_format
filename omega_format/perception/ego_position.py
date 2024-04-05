import numpy as np
from h5py import Group
from pydantic import field_validator, model_validator, Field

from .valvar import ValVar
from ..settings import get_settings
from ..reference_resolving import InputClassBase
import pydantic_numpy.typing as pnd


class EgoPosition(InputClassBase):
    yaw_rate: pnd.NpNDArray
    pitch: pnd.NpNDArray
    heading: ValVar = Field(default_factory=ValVar)
    pos_longitude: ValVar = Field(default_factory=ValVar)
    pos_latitude: ValVar = Field(default_factory=ValVar)
    pos_z: ValVar = Field(default_factory=ValVar)


    @field_validator('yaw_rate','pitch')
    @classmethod
    def check_array_length(cls, v):
        assert v.shape[0]>0, 'size zero polyline'
        return v
    
    @model_validator(mode='after')
    def check_same_length(self):
        assert self.pos_x.shape[0]==self.pos_y.shape[0]==self.pos_z.shape[0], 'Polyline has coordinates of different length'
        return self

    @field_validator('heading')
    @classmethod
    def check_angle(cls, v):
        for val in v.val:
            assert val.size>0 and -360 <= val <= 360, f'{val} is not a valid angle'
        return v

    @field_validator('pos_longitude')
    @classmethod
    def check_longitude(cls, v):
        assert np.all(np.logical_and(v>=-180, v<=180)), 'invalide longitude value found'
        return v

    @field_validator('pos_latitude')
    @classmethod
    def check_latitude(cls, v):
        assert np.all(np.logical_and(v>=-90, v<=90)), 'invalide latitude value found'
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            heading=ValVar.from_hdf5(group['heading'], validate=validate),
            pos_longitude=ValVar.from_hdf5(group['posLongitude'], validate=validate),
            pos_latitude=ValVar.from_hdf5(group['posLatitude'], validate=validate),
            pos_z=ValVar.from_hdf5(group['posZ'], validate=validate),
            yaw_rate=group['yawRate'][()].astype(float),
            pitch=group['pitch'][()].astype(float),
        )
        return self

    def to_hdf5(self, group: Group):
        self.heading.to_hdf5(group.create_group('heading'))
        self.pos_longitude.to_hdf5(group.create_group('posLongitude'))
        self.pos_latitude.to_hdf5(group.create_group('posLatitude'))
        self.pos_z.to_hdf5(group.create_group('posZ'))
        group.create_dataset('yawRate', data=self.yaw_rate, **get_settings().hdf5_compress_args)
        group.create_dataset('pitch', data=self.pitch, **get_settings().hdf5_compress_args)
