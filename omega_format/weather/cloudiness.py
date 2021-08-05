from pydantic import validator
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..pydantic_utils.pydantic_config import PydanticConfig


class Cloudiness(InputClassBase):
    degree: np.ndarray = np.array([])
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @validator('degree')
    def check_cloudiness_degree(cls, v):
        for value in v:
            assert 0 <= value <= 8, f'cloudiness should be given in numerators of eights (0 to 8), but is {value}'
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = func(
            degree=group['degree'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('degree', data=self.degree)
        group.attrs.create('source', data=self.source)

    @property
    def is_cloudy(self):
        degree = np.mean(self.degree)
        return degree >= 2
