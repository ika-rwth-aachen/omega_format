from pydantic import validator
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..pydantic_utils.pydantic_config import PydanticConfig


class Temperature(InputClassBase):
    air_temp: np.ndarray = np.array([])
    air_temp_5cm: np.ndarray = np.array([])
    ground_temp: np.ndarray = np.array([])
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @validator('air_temp', 'air_temp_5cm', 'ground_temp')
    def check_temperature(cls, v):
        for value in v:
            assert -50 <= value <= 50, f"temperature should be between -50 and +50 degrees celsius, but is {value}"
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = cls(
            air_temp=group['airTemp'][()],
            air_temp_5cm=group['airTemp5cm'][()],
            ground_temp=group['groundTemp'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('airTemp', data=self.air_temp)
        group.create_dataset('airTemp5cm', data=self.air_temp_5cm)
        group.create_dataset('groundTemp', data=self.ground_temp)
        group.attrs.create('source', data=self.source)

    def get_avg_temp(self):
        return np.mean(self.air_temp)
