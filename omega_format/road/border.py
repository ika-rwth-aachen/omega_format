from h5py import Group

from ..geometry.polyline import Polyline
from ..reference_resolving import InputClassBase, raise_not_resolved


class Border(InputClassBase):
    polyline: Polyline

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        return input_recording.roads[i[0]].borders[i[1]]

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            polyline=Polyline.from_hdf5(group),
        )
        return self

    def to_hdf5(self, group: Group):
        self.polyline.to_hdf5(group)
