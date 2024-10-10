from h5py import Group
from pydantic import model_validator
from ..settings import get_settings
from ..reference_resolving import InputClassBase
import pydantic_numpy.typing as pnd

class ValVar(InputClassBase):
    val: pnd.NpNDArray
    var: pnd.NpNDArray
    
    @model_validator(mode='after')
    def check_array_same_size(self):
        assert self.val.shape[0]>0 and self.val.shape[0]==self.var.shape[0], 'val var do not match up'
        return self

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
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