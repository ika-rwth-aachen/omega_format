from pydantic.fields import Field
from pydantic import validator
from typing import List
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..pydantic_utils.pydantic_config import PydanticConfig


class GustOfWind(InputClassBase):
    wind_speed: np.ndarray = np.array([])
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN
    type: List[ReferenceTypes.GustOfWind] = Field(default_factory=lambda: [ReferenceTypes.GustOfWind.NO_GUSTS_OF_WIND])

    @validator('wind_speed')
    def check_wind_speed(cls, v):
        for value in v:
            assert 0 <= value <= 120, f"wind speed should be between 0 and 120 m/s, but is {value}"
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = cls(
            wind_speed=group['windSpeed'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
            type=list(map(ReferenceTypes.GustOfWind, group['type'][()].tolist()))
        )
        return self

    def to_hdf5(self, group: Group):
        group.attrs.create('source', data=self.source)
        group.create_dataset('type', data=self.type)
        group.create_dataset('windSpeed', data=self.wind_speed)
