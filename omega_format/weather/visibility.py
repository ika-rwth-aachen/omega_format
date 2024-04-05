from pydantic import field_validator, Field
import numpy as np
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..settings import get_settings
import pydantic_numpy.typing as pnd

class Visibility(InputClassBase):
    visibility: pnd.NpNDArray = Field(default_factory=np.array)
    source: ReferenceTypes.WeatherSource = ReferenceTypes.WeatherSource.UNKNOWN

    @field_validator('visibility')
    @classmethod
    def check_visibility(cls, v):
        for value in v:
            assert 0 <= value <= 30000, f"visibility should be between 0 and 30000 meters, but is {value}"
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            visibility=group['visibility'][()],
            source=ReferenceTypes.WeatherSource(group.attrs["source"]),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('visibility', data=self.visibility, **get_settings().hdf5_compress_args)
        group.attrs.create('source', data=self.source)
