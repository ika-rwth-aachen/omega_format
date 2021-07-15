from pydantic import BaseModel

from ..pydantic_utils.pydantic_config import PydanticConfig
from h5py import Group


class Position(BaseModel):
    class Config(PydanticConfig):
        pass
    pos_x: float
    pos_y: float
    pos_z: float

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = func(
            pos_x=group['posX'][()].astype(float),
            pos_y=group['posY'][()].astype(float),
            pos_z=group['posZ'][()].astype(float)
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('posX', data=self.pos_x)
        group.create_dataset('posY', data=self.pos_y)
        group.create_dataset('posZ', data=self.pos_z)
