from pydantic.dataclasses import Field
from pydantic import validator
import numpy as np
from h5py import Group
from typing import List

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..pydantic_utils.pydantic_config import PydanticConfig


class Wind(InputClassBase):
    type: List[ReferenceTypes.Wind] = Field(default_factory=lambda: [ReferenceTypes.Wind.CALM])
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN
    wind_direction: np.ndarray = np.array([])
    wind_speed: np.ndarray = np.array([])

    @validator('wind_direction')
    def check_degree(cls, v):
        for value in v:
            assert isinstance(value, float), f'wind direction should be of type float, but is {type(value)}: {value}'
            assert 0 <= value <= 360, f"wind direction should range from 0 to 360 degrees, but is {value}"
        return v

    @validator('wind_speed')
    def check_wind_speed(cls, v):
        for value in v:
            assert isinstance(value, float), f'wind speed should be of type float, but is {type(value)}: {value}'
            assert 0 <= value <= 50, f'wind speed should range from 0 to 50 m/s, but is {value}'
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = func(
            wind_speed=np.array(group['windSpeed'][()], dtype=float),
            wind_direction=np.array(group['windDirection'][()], dtype=float),
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
            type=list(map(ReferenceTypes.Wind, group['type'][()].tolist()))
        )
        return self

    def to_hdf5(self, group: Group):
        group.attrs.create('source', data=self.source)
        group.create_dataset('type', data=self.type)
        group.create_dataset('windDirection', data=self.wind_direction)
        group.create_dataset('windSpeed', data=self.wind_speed)

    @property
    def is_windy(self):
        most_frequent_type = max(set(self.type), key=self.type.count, default=None)
        return most_frequent_type in [ReferenceTypes.Wind.MODERATE_BREEZE,
                                      ReferenceTypes.Wind.FRESH_BREEZE,
                                      ReferenceTypes.Wind.STRONG_BREEZE,
                                      ReferenceTypes.Wind.NEAR_GALE,
                                      ReferenceTypes.Wind.GALE,
                                      ReferenceTypes.Wind.STRONG_GALE,
                                      ReferenceTypes.Wind.STORM,
                                      ReferenceTypes.Wind.VIOLENT_STORM,
                                      ReferenceTypes.Wind.HURRICANE]
