from pydantic import validator
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..pydantic_utils.pydantic_config import PydanticConfig


class Solar(InputClassBase):
    diff_solar_radiation: np.ndarray = np.array([])
    longwave_down_radiation: np.ndarray = np.array([])
    solar_hours: np.ndarray = np.array([])
    solar_incoming_radiation: np.ndarray = np.array([])
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @validator('solar_hours')
    def check_solar_hours(cls, v):
        for value in v:
            assert 0 <= value <= 24, f"solar hours should be between 0 and 24 h, bus is {value}"
        return v

    #  TODO Sanity checks for Radiation

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = cls(
            diff_solar_radiation=group['diffSolarRadiation'][()],
            longwave_down_radiation=group['longwaveDownRadiation'][()],
            solar_hours=group['solarHours'][()],
            solar_incoming_radiation=group['solarIncomingRadiation'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('diffSolarRadiation', data=self.diff_solar_radiation)
        group.create_dataset('longwaveDownRadiation', data=self.longwave_down_radiation)
        group.create_dataset('solarHours', data=self.solar_hours)
        group.create_dataset('solarIncomingRadiation', data=self.solar_incoming_radiation)
        group.attrs.create('source', data=self.source)

    @property
    def is_sunny(self):
        solar_hours = np.mean(self.solar_hours)
        return solar_hours >= 30
