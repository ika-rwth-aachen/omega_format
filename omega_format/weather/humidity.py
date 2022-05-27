from pydantic import validator, Field
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..pydantic_utils.pydantic_config import PydanticConfig


class Humidity(InputClassBase):
    humidity: np.ndarray = Field(default=np.array([]))
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @validator('humidity')
    def check_humidity(cls, v):
        for value in v:
            assert 0 <= value <= 100, f"humidity should be between 0 and 100 %, but is {value}"
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = func(
            humidity=group['humidity'][()],
            source=group.attrs["source"]
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('humidity', data=self.humidity)
        group.attrs.create('source', data=self.source)

    @property
    def is_foggy(self):
        humidity = np.mean(self.humidity)
        return humidity > 95
