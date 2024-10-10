from pydantic import field_validator
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..settings import get_settings
import pydantic_numpy.typing as pnd


class Cloudiness(InputClassBase):
    degree: pnd.NpNDArray
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @field_validator('degree')
    @classmethod
    def check_cloudiness_degree(cls, v):
        for value in v:
            assert value.size==0 or 0 <= value <= 8, f'cloudiness should be given in numerators of eights (0 to 8), but is {value}'
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            degree=group['degree'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('degree', data=self.degree, **get_settings().hdf5_compress_args)
        group.attrs.create('source', data=self.source)

    @property
    def is_cloudy(self):
        try:
            degree = np.mean(self.degree)
            return degree >= 2
        except FloatingPointError:
            return False
