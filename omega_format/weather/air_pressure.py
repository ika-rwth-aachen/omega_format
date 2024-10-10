from pydantic import field_validator
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..settings import get_settings
import pydantic_numpy.typing as pnd


class AirPressure(InputClassBase):
    air_pressure_nn: pnd.NpNDArray
    air_pressure_zero: pnd.NpNDArray
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @field_validator('air_pressure_nn', 'air_pressure_zero')
    @classmethod
    def check_air_pressure_plausibility(cls, v):
        for value in v:
            assert value.size==0 or 500 <= value <= 1100, \
                f'air pressure value is not plausible, should be between 500 and 1100 hPa, is {value}'
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            air_pressure_nn=group["airPressureNN"][:],
            air_pressure_zero=group["airPressureZero"][:],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('airPressureNN', data=self.air_pressure_nn, **get_settings().hdf5_compress_args)
        group.create_dataset('airPressureZero', data=self.air_pressure_zero, **get_settings().hdf5_compress_args)
        group.attrs.create('source', data=self.source)
