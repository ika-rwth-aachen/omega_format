import numpy as np
from h5py import Group
from pydantic import Field
from ..reference_resolving import InputClassBase


class RoadCondition(InputClassBase):
    maintenance_status: np.ndarray = Field(default=np.array([], dtype=np.float64))
    spray: np.ndarray = Field(default=np.array([], dtype=np.float64))
    surface_condition: np.ndarray = Field(default=np.array([], dtype=np.float64))

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.construct
        self = func(
            maintenance_status=group['maintenanceStatus'][()],
            spray=group['spray'][()],
            surface_condition=group['surfaceCondition'][()]
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('maintenanceStatus', data=self.maintenance_status)
        group.create_dataset('spray', data=self.spray)
        group.create_dataset('surfaceCondition', data=self.surface_condition)
