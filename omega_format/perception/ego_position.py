from warnings import warn
import numpy as np
from h5py import Group
from pydantic import validator, Field, BaseModel

from .valvar import ValVar
from ..pydantic_utils.pydantic_config import PydanticConfig


class EgoPosition(BaseModel):
    class Config(PydanticConfig):
        pass
    heading: ValVar = Field(default_factory=ValVar)
    pos_longitude: ValVar = Field(default_factory=ValVar)
    pos_latitude: ValVar = Field(default_factory=ValVar)
    pos_z: ValVar = Field(default_factory=ValVar)
    yaw_rate: np.ndarray = Field(default=np.array([], dtype=np.float64))
    pitch: np.ndarray = Field(default=np.array([], dtype=np.float64))

    if False:
        @validator('heading', 'pos_longitude', 'pos_latitude')
        def check_array_length(cls, v, values):
            if isinstance(v, ValVar):
                assert len(v.val) == len(v.var), f'length of val {len(v.val)} and length of var {len(v.var)} are not the same'
                return v
            else:
                if not len(v) > 0:
                    warn('received trajectory with empty array')

                if len(values) > 0:
                    # first array would be validated if len(values)=0 -> no length to compare against
                    # use the length of pos_x to check equality with other array length
                    length = len(values.get('heading'))
                    if len(v) != length:
                        raise ValueError(f'length of all EgoPosition arrays must match, expected len {len(v)}, actual len {length}')
            return v

    @validator('heading')
    def check_angle(cls, v):
        for val in v.val:
            assert val.size>0 and -360 <= val <= 360, f'{val} is not a valid angle'
        return v

    @validator('pos_longitude')
    def check_longitude(cls, v):
        for val in v.val:
            assert val.size>0 and -180 <= val <= 180, f'{val} is not a valid longitude value, should be between -180 and 180 degrees'
        return v

    @validator('pos_latitude')
    def check_latitude(cls, v):
        for val in v.val:
            assert val.size>0 -90 <= val <= 90, f'{val} is not a valid latitude value, should be between -180 and 180 degrees'
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.construct
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
        group.create_dataset('yawRate', data=self.yaw_rate)
        group.create_dataset('pitch', data=self.pitch)
