from pydantic import validator, Field
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..pydantic_utils.pydantic_config import PydanticConfig
from ..settings import get_settings

class Temperature(InputClassBase):
    air_temp: np.ndarray = Field(default=np.array([], dtype=np.float64))
    air_temp_5cm: np.ndarray = Field(default=np.array([], dtype=np.float64))
    ground_temp: np.ndarray = Field(default=np.array([], dtype=np.float64))
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @validator('air_temp', 'air_temp_5cm', 'ground_temp')
    def check_temperature(cls, v):
        for value in v:
            assert -50 <= value <= 50, f"temperature should be between -50 and +50 degrees celsius, but is {value}"
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.construct
        self = cls(
            air_temp=group['airTemp'][()],
            air_temp_5cm=group['airTemp5cm'][()],
            ground_temp=group['groundTemp'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('airTemp', data=self.air_temp, **get_settings().hdf5_compress_args)
        group.create_dataset('airTemp5cm', data=self.air_temp_5cm, **get_settings().hdf5_compress_args)
        group.create_dataset('groundTemp', data=self.ground_temp, **get_settings().hdf5_compress_args)
        group.attrs.create('source', data=self.source)

    def get_avg_temp(self):
        try:
            return np.mean(self.air_temp)
        except FloatingPointError:
            return np.nan
