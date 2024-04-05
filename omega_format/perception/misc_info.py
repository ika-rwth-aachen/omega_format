from pydantic import Field
from h5py import Group

from ..settings import get_settings
from typing_extensions import Annotated
from ..reference_resolving import InputClassBase

class MiscInfo(InputClassBase):
    id: Annotated[int, Field(ge=0)] = 0
    light_intensity: Annotated[float, Field(ge=0)] = 0.
    acoustics: Annotated[float, Field(ge=0)] = 0.

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        sub_group_name = group.name.rpartition('/')[-1]
        self = func(
            id=int(sub_group_name),
            light_intensity=group['lightIntensity'][()].astype(float),
            acoustics=group['acoustics'][()].astype(float),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('lightIntensity', data=self.light_intensity, **get_settings().hdf5_compress_args)
        group.create_dataset('acoustics', data=self.acoustics, **get_settings().hdf5_compress_args)
