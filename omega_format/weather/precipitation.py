from pydantic.dataclasses import Field
from typing import List
from pydantic import field_validator
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..settings import get_settings
import pydantic_numpy.typing as pnd


class Precipitation(InputClassBase):
    type: List[ReferenceTypes.Precipitation] = Field(default_factory=lambda: [ReferenceTypes.Precipitation.NO_RAIN])
    amount_hourly: pnd.NpNDArray = Field(default_factory=np.array)
    amount_minute: pnd.NpNDArray = Field(default_factory=np.array)
    new_snow_depth: pnd.NpNDArray = Field(default_factory=np.array)
    snow_depth: pnd.NpNDArray = Field(default_factory=np.array)
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @field_validator('amount_hourly')
    @classmethod
    def check_hourly_precipitation(cls, v):
        for value in v:
            assert 0 <= value <= 300, f"hourly precipitation should be between 0 and 300 mm, but is {value}"
        return v

    @field_validator('amount_minute')
    @classmethod
    def check_minute_precipitation(cls, v):
        for value in v:
            assert 0 <= value <= 20, f"per minute precipitation should be between 0 and 20 mm, but is {value}"
        return v

    @field_validator('snow_depth')
    @classmethod
    def check_snow_depth(cls, v):
        for value in v:
            assert 0 <= value <= 200, f"snow depth should be between 0 and 200 cm, but is {value}"
        return v

    @field_validator('new_snow_depth')
    @classmethod
    def check_new_snow_depth(cls, v):
        for value in v:
            assert 0 <= value <= 100, f"new snow depth should be between 0 and 100 cm, but is {value}"
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            amount_hourly=group['amountHourly'][()],
            amount_minute=group['amountMinute'][()],
            new_snow_depth=group['newSnowDepth'][()],
            snow_depth=group['snowDepth'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
            type=list(map(ReferenceTypes.Precipitation, group['type'][()].tolist()))
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('amountHourly', data=self.amount_hourly, **get_settings().hdf5_compress_args)
        group.create_dataset('amountMinute', data=self.amount_minute, **get_settings().hdf5_compress_args)
        group.create_dataset('newSnowDepth', data=self.new_snow_depth, **get_settings().hdf5_compress_args)
        group.create_dataset('snowDepth', data=self.snow_depth, **get_settings().hdf5_compress_args)
        group.attrs.create('source', data=self.source)
        group.create_dataset('type', data=self.type, **get_settings().hdf5_compress_args)

    @property
    def is_raining(self):
        most_frequent_type = max(set(self.type), key=self.type.count, default=None)
        return most_frequent_type in [ReferenceTypes.Precipitation.LIGHT_RAIN,
                                      ReferenceTypes.Precipitation.MODERATE_RAIN,
                                      ReferenceTypes.Precipitation.HEAVY_RAIN]

    @property
    def is_thunderstorm(self):
        most_frequent_type = max(set(self.type), key=self.type.count, default=None)
        return most_frequent_type in [ReferenceTypes.Precipitation.EXTREMELY_HEAVY_RAIN]

    @property
    def is_snowing(self):
        most_frequent_type = max(set(self.type), key=self.type.count, default=None)
        return most_frequent_type in [ReferenceTypes.Precipitation.LIGHT_SNOW,
                                      ReferenceTypes.Precipitation.MODERATE_SNOW,
                                      ReferenceTypes.Precipitation.HEAVY_SNOW]
