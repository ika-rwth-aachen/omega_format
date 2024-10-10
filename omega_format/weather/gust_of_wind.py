from pydantic import field_validator, Field
from typing import List
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..settings import get_settings
import pydantic_numpy.typing as pnd


class GustOfWind(InputClassBase):
    wind_speed: pnd.NpNDArray
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN
    type: List[ReferenceTypes.GustOfWind] = Field(default_factory=lambda: [ReferenceTypes.GustOfWind.NO_GUSTS_OF_WIND])

    @field_validator('wind_speed')
    @classmethod
    def check_wind_speed(cls, v):
        for value in v:
            assert 0 <= value <= 120, f"wind speed should be between 0 and 120 m/s, but is {value}"
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            wind_speed=group['windSpeed'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
            type=list(map(ReferenceTypes.GustOfWind, group['type'][()].tolist()))
        )
        return self

    def to_hdf5(self, group: Group):
        group.attrs.create('source', data=self.source)
        group.create_dataset('type', data=self.type, **get_settings().hdf5_compress_args)
        group.create_dataset('windSpeed', data=self.wind_speed, **get_settings().hdf5_compress_args)
