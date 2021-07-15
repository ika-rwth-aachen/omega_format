from warnings import warn

import numpy as np
from h5py import Group
from pydantic import validator, BaseModel

from ..pydantic_utils.pydantic_config import PydanticConfig


class ValVar(BaseModel):
    class Config(PydanticConfig):
        pass
    val: np.ndarray = np.array([])
    var: np.ndarray = np.array([])

    @validator('var')
    def check_array_length(cls, v, values):
        if not len(v) > 0:
            warn('received empty array in ValVar class')

        length = len(values.get('val'))
        if len(v) != length:
            raise ValueError(
                f'length of var array must match with val array, expected len {len(v)}, actual len {length}')
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = func(
            val=group['val'][()],
            var=group['var'][()],
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('val', data=self.val)
        group.create_dataset('var', data=self.var)

    def cut_to_timespan(self, birth, death):
        assert birth >= 0
        assert birth <= death

        if len(self.val) > 0:
            assert len(self.val) > birth
            assert len(self.val) > death
            self.val = self.val[birth:death + 1]

        if len(self.var) > 0:
            assert len(self.var) > birth
            assert len(self.var) > death
            self.var = self.var[birth:death + 1]
