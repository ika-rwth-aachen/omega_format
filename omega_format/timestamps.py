import numpy as np
from .reference_resolving import InputClassBase
import pydantic_numpy.typing as pnd


class Timestamps(InputClassBase):
    val: pnd.NpNDArray

    def cut_to_timespan(self, birth, death):
        self.val = self.val[birth:death+1]

    @classmethod
    def create(cls, duration, update_rate):
        self = cls(
            val=np.arange(start=0, stop=duration, step=update_rate)
        )
        return self
