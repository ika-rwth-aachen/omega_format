from pydantic import validator
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..pydantic_utils.pydantic_config import PydanticConfig


class AirPressure(InputClassBase):
    air_pressure_nn: np.ndarray = np.array([])
    air_pressure_zero: np.ndarray = np.array([])
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @validator('air_pressure_nn', 'air_pressure_zero')
    def check_air_pressure_plausibility(cls, v):
        for value in v:
            assert value.size==0 or 500 <= value <= 1100, \
                f'air pressure value is not plausible, should be between 500 and 1100 hPa, is {value}'
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = func(
            air_pressure_nn=group["airPressureNN"][:],
            air_pressure_zero=group["airPressureZero"][:],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('airPressureNN', data=self.air_pressure_nn)
        group.create_dataset('airPressureZero', data=self.air_pressure_zero)
        group.attrs.create('source', data=self.source)
