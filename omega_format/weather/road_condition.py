import numpy as np
from h5py import Group
from pydantic import Field
from ..reference_resolving import InputClassBase
from ..settings import get_settings
import pydantic_numpy.typing as pnd


class RoadCondition(InputClassBase):
    maintenance_status: pnd.NpNDArray = Field(default_factory=np.array)
    spray: pnd.NpNDArray = Field(default_factory=np.array)
    surface_condition: pnd.NpNDArray = Field(default_factory=np.array)

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            maintenance_status=group['maintenanceStatus'][()],
            spray=group['spray'][()],
            surface_condition=group['surfaceCondition'][()]
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('maintenanceStatus', data=self.maintenance_status, **get_settings().hdf5_compress_args)
        group.create_dataset('spray', data=self.spray)
        group.create_dataset('surfaceCondition', data=self.surface_condition, **get_settings().hdf5_compress_args)
