from pydantic import field_validator
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..settings import get_settings
import pydantic_numpy.typing as pnd


class Humidity(InputClassBase):
    humidity: pnd.NpNDArray
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @field_validator('humidity')
    @classmethod
    def check_humidity(cls, v):
        for value in v:
            assert 0 <= value <= 100, f"humidity should be between 0 and 100 %, but is {value}"
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            humidity=group['humidity'][()],
            source=group.attrs["source"]
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('humidity', data=self.humidity, **get_settings().hdf5_compress_args)
        group.attrs.create('source', data=self.source)

    @property
    def is_foggy(self):
        try:
            humidity = np.mean(self.humidity)
            return humidity > 95
        except FloatingPointError:
            return False
