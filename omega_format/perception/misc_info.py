from pydantic import BaseModel
from pydantic.types import conint, confloat
from h5py import Group

from ..pydantic_utils.pydantic_config import PydanticConfig


class MiscInfo(BaseModel):
    class Config(PydanticConfig):
        pass
    id: conint(ge=0) = 0
    light_intensity: confloat(ge=0) = 0.
    acoustics: confloat(ge=0) = 0.

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        sub_group_name = group.name.rpartition('/')[-1]
        self = func(
            id=int(sub_group_name),
            light_intensity=group['lightIntensity'][()].astype(float),
            acoustics=group['acoustics'][()].astype(float),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('lightIntensity', data=self.light_intensity)
        group.create_dataset('acoustics', data=self.acoustics)
