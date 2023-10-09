from warnings import warn

import numpy as np
from h5py import Group
from pydantic import validator, BaseModel, Field

from ..pydantic_utils.pydantic_config import PydanticConfig
from ..settings import get_settings
from numpy.typing import NDArray
class ValVar(BaseModel):
    class Config(PydanticConfig):
        arbitrary_types_allowed=True
    val: NDArray[np.floating] = Field(default=np.array([]))
    var: NDArray[np.floating] = Field(default=np.array([]))
    
    @validator('val')
    def check_zero_or_same_length(cls, v, values):
        pass

    @validator('var')
    def check_array_length(cls, v, values):
        if not v.size > 0:
            warn('received empty array in ValVar class')

        length = len(values.get('val'))
        if len(v) != length:
            warn('lenght of var does not match length of val. This is only possible if var is of type not_provided')
            # raise ValueError(
            #     f'length of var array must match with val array, expected len {len(v)}, actual len {length}')
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.construct
        self = func(
            val=group['val'][()],
            var=group['var'][()],
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('val', data=self.val, **get_settings().hdf5_compress_args)
        group.create_dataset('var', data=self.var, **get_settings().hdf5_compress_args)

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
pass