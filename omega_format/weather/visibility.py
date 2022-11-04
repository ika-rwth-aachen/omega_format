from pydantic import validator, Field
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..pydantic_utils.pydantic_config import PydanticConfig


class Visibility(InputClassBase):
    visibility: np.ndarray = Field(default=np.array([], dtype=np.float64))
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @validator('visibility')
    def check_visibility(cls, v):
        for value in v:
            assert 0 <= value <= 30000, f"visibility should be between 0 and 30000 meters, but is {value}"
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.construct
        self = func(
            visibility=group['visibility'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('visibility', data=self.visibility)
        group.attrs.create('source', data=self.source)
