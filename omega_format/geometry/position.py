from h5py import Group
from ..reference_resolving import InputClassBase

class Position(InputClassBase):
    pos_x: float
    pos_y: float
    pos_z: float

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
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
