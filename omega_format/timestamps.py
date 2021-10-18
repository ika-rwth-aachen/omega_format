import numpy as np

from .reference_resolving import InputClassBase


class Timestamps(InputClassBase):
    val: np.ndarray = np.array([], dtype=np.float64)# np.ndarray = np.array([0])

    def cut_to_timespan(self, birth, death):
        self.val = self.val[birth:death+1]

    @classmethod
    def create(cls, duration, update_rate):
        self = cls(
            val=np.arange(start=0, stop=duration, step=update_rate)
        )
        return self
