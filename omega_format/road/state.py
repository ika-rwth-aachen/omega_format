from copy import deepcopy, copy
from h5py import Group

from ..reference_resolving import InputClassBase, ReferenceElement
from ..settings import get_settings
import pydantic_numpy.typing as pnd

class State(InputClassBase):
    sign: ReferenceElement
    value: pnd.NpNDArray

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        from .sign import Sign
        func = cls if validate else cls.model_construct
        self = func(
            sign=ReferenceElement(group.attrs["referenceId"], Sign),
            value=group['value'][()],
        )
        return self

    def resolve(self, input_recording=None):
        super().resolve(input_recording=input_recording)
        self.sign.state = self

    def cut_to_timespan(self, birth, death):
        self.values = self.values[birth:death+1]

    def __deepcopy__(self, memodict={}):
        from .sign import Sign
        dp = copy(self)
        dp.sign = ReferenceElement(self.sign.reference, Sign)
        dp.value = deepcopy(self.values, memodict)
        return dp

    def to_hdf5(self, group: Group):
        group.create_dataset('referenceId', data=self.sign.reference)
        group.create_dataset('value', data=self.values, **get_settings().hdf5_compress_args)
