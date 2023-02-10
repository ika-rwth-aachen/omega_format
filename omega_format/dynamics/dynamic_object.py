from dataclasses import fields
from pydantic import conint
from pydantic.fields import Field

import numpy as np

from .bounding_box import BoundingBox
from .trajectory import Trajectory
from ..settings import DefaultValues
from ..enums import ReferenceTypes
from ..geometry import BBXCornersClass
from ..reference_resolving import *
import xarray as xr
from typing import Optional
from h5py import Group

def in_timespan(obj, birth, death):
    """
    birth = first timestamp idx
    death = last timestamp idx
    """
    return birth <= obj.end and death >= obj.birth


def timespan_to_cutoff_idxs(obj, birth, death):
    start_delay = max(0, obj.birth - birth)
    cutoff_start = int(max(0, birth - obj.birth))
    cutoff_end = int(min(obj.end - obj.birth + 1, death - birth - start_delay + cutoff_start + 1))

    own_birth = start_delay
    own_death = cutoff_end - cutoff_start + start_delay - 1

    assert cutoff_start <= cutoff_end
    assert own_birth >= 0
    assert own_death <= death - birth
    assert own_birth <= own_death

    return cutoff_start, cutoff_end, own_birth


class DynamicObject(InputClassBase, BBXCornersClass):
    bb: BoundingBox = Field(default_factory=BoundingBox)
    tr: Trajectory = Field(default_factory=Trajectory)
    birth: conint(ge=0)
    connected_to: Optional[ReferenceElement] = None
    attached_to: Optional[ReferenceElement] = None
    """first timestamp idx"""

    @property
    def end(self):
        """Last timestamp idx"""
        return len(self.tr.pos_x) + self.birth - 1

    def in_timespan(self, birth, death):
        return in_timespan(self, birth, death)

    def timespan_to_cutoff_idxs(self, birth, death):
        return timespan_to_cutoff_idxs(self, birth, death)

    def cut_to_timespan(self, birth, death):
        cutoff_start, cutoff_end, own_birth = self.timespan_to_cutoff_idxs(birth, death)
        self.birth = own_birth
        for k, v in vars(self.tr).items():
            if isinstance(v, np.ndarray):
                try:
                    setattr(self.tr, k, v[..., cutoff_start:cutoff_end])
                except ValueError:
                    # most likely it was tried to set a cached property
                    # TODO: find a way to exclude cached properties from loop
                    pass

        # cut properties from BBXCornersClass
        for k, v in vars(self).items():
            if isinstance(v, np.ndarray):
                setattr(self, k, v[..., cutoff_start:cutoff_end])

    @property
    def length(self):
        if self.bb.length == 0:
            if self.type == ReferenceTypes.RoadUserType.BICYCLE:
                return BoundingBox(DefaultValues.bicycle).length
            elif self.type == ReferenceTypes.RoadUserType.PEDESTRIAN:
                return BoundingBox(DefaultValues.pedestrian).length
            else:
                return .2  # TODO handle better
        else:
            return self.bb.length

    @property
    def width(self):
        if self.bb.width == 0:
            if self.type == ReferenceTypes.RoadUserType.BICYCLE:
                return BoundingBox(DefaultValues.bicycle).width
            elif self.type == ReferenceTypes.RoadUserType.PEDESTRIAN:
                return BoundingBox(DefaultValues.pedestrian).width
            else:
                return .2  # TODO handle better
        else:
            return self.bb.width

    def to_xarray(self, rr):
        return xr.Dataset({f: ('time', getattr(self.tr,f)) for f in self.tr.__fields__.keys()},
                          coords={'time':rr.timestamps.val[self.birth:self.end+1]})

    def to_hdf5(self, group: Group):
        group.attrs.create('birthStamp', data=self.birth)
        if self.connected_to is not None:
            group.attrs.create('connectedTo', data=self.connected_to.reference)
        else:
            group.attrs.create('connectedTo', data=-1)
        if self.attached_to is not None:
            group.attrs.create('attachedTo', data=self.connected_to.reference)
        else:
            group.attrs.create('attachedTo', data=-1)
        self.bb.to_hdf5(group.create_group('boundBox'))
        self.tr.to_hdf5(group.create_group('trajectory'))
