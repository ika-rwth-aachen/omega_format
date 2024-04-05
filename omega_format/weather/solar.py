from pydantic import field_validator, Field
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..settings import get_settings
import pydantic_numpy.typing as pnd


class Solar(InputClassBase):
    diff_solar_radiation: pnd.NpNDArray = Field(default_factory=np.array)
    longwave_down_radiation: pnd.NpNDArray = Field(default_factory=np.array)
    solar_hours: pnd.NpNDArray = Field(default_factory=np.array)
    solar_incoming_radiation: pnd.NpNDArray = Field(default_factory=np.array)
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @field_validator('solar_hours')
    @classmethod
    def check_solar_hours(cls, v):
        for value in v:
            assert 0 <= value <= 24, f"solar hours should be between 0 and 24 h, bus is {value}"
        return v

    #  TODO Sanity checks for Radiation

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            diff_solar_radiation=group['diffSolarRadiation'][()],
            longwave_down_radiation=group['longwaveDownRadiation'][()],
            solar_hours=group['solarHours'][()],
            solar_incoming_radiation=group['solarIncomingRadiation'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('diffSolarRadiation', data=self.diff_solar_radiation, **get_settings().hdf5_compress_args)
        group.create_dataset('longwaveDownRadiation', data=self.longwave_down_radiation, **get_settings().hdf5_compress_args)
        group.create_dataset('solarHours', data=self.solar_hours, **get_settings().hdf5_compress_args)
        group.create_dataset('solarIncomingRadiation', data=self.solar_incoming_radiation, **get_settings().hdf5_compress_args)
        group.attrs.create('source', data=self.source)

    @property
    def is_sunny(self):
        try:
            solar_hours = np.mean(self.solar_hours)
            return solar_hours >= 30
        except FloatingPointError:
            return False
