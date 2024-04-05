from pydantic import field_validator, Field
import numpy as np
from h5py import Group
from ..reference_resolving import InputClassBase
import pydantic_numpy.typing as pnd

class BoundingBox(InputClassBase):
    vec: pnd.NpNDArray
    confident_length: bool = True
    confident_width: bool = True

    @field_validator('vec')
    @classmethod
    def parse_values(cls, v):
        assert v.size==0 or np.all(v > 0), f'bounding box size should be greater zero, but is {v}'
        # print(f"Min: {np.min(v)}, Max: {np.max(v)}")
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate=True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            confident_length=group['length'].attrs["confident"],
            confident_width=group['width'].attrs["confident"],
            vec=np.array([group['length'][()],
                          group['width'][()],
                          group['height'][()]])
        )
        return self

    @property
    def length(self):
        return self.vec[0]

    @property
    def width(self):
        return self.vec[1]

    @property
    def height(self):
        return self.vec[2]

    def to_hdf5(self, group: Group):
        dset_length = group.create_dataset('length', data=self.length)
        dset_width = group.create_dataset('width', data=self.width)
        _ = group.create_dataset('height', data=self.height)
        dset_length.attrs["confident"] = self.confident_length
        dset_width.attrs["confident"] = self.confident_width
