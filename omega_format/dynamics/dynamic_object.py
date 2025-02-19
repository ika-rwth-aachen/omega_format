from typing import Optional

import numpy as np
import shapely
import xarray as xr
from h5py import Group
from pydantic import Field
from typing_extensions import Annotated

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase, ReferenceElement
from ..settings import DefaultValues
from .bounding_box import BoundingBox
from .trajectory import Trajectory


def rot_x(x, y, phi):
    return x * np.cos(phi) - y * np.sin(phi)


def rot_y(x, y, phi):
    return x * np.sin(phi) + y * np.cos(phi)


def rot_point(orig_x, orig_y, x, y, phi):
    return np.array([orig_x + rot_x(x, y, phi), orig_y + rot_y(x, y, phi)])

def in_timespan(obj, birth, death):
    """
    birth = first timestamp idx
    death = last timestamp idx
    """
    return bool(birth <= obj.end and death >= obj.birth)


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


class DynamicObject(InputClassBase):
    bb: BoundingBox = Field(default_factory=BoundingBox)
    tr: Trajectory = Field(default_factory=Trajectory)
    birth: Annotated[int, Field(ge=0)]
    connected_to: Optional[ReferenceElement] = None
    attached_to: Optional[ReferenceElement] = None

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

    def to_xarray(self):
        if self.timestamps is None:
            raise RuntimeError('You have to run `set_timestamps()` of the associated recording')
        return xr.Dataset({k: ('time', v) for k, v in self.tr.model_dump().items()},
                          coords={'time': self.timestamps})

    def _set_timestamps(self, rr):
        self.timestamps = rr.timestamps[self.birth:self.end+1]
    
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

    def model_post_init(self, __context):
        self._set_corners_and_polygon()
        
    def _set_corners_and_polygon(self):
        try:
            heading = self.tr.heading / 180 * np.pi
            x = self.tr.pos_x
            y = self.tr.pos_y
        except AttributeError as e:
            try:
                heading = self.heading / 180 * np.pi
                x = self.position.pos_x
                y = self.position.pos_y
            except AttributeError as ee:
                raise AttributeError('Object must either have property Trajectory or position') from (e, ee)
        c2f = self.length / 2
        c2l = self.width / 2
        front_left = rot_point(x, y, +c2f, +c2l, heading).T
        front_right = rot_point(x, y, +c2f, -c2l, heading).T
        back_right = rot_point(x, y, -c2f, -c2l, heading).T
        back_left = rot_point(x, y, -c2f, +c2l, heading).T
        self.tr.polygon = shapely.polygons(np.stack([front_left, front_right, back_right, back_left]).swapaxes(0,1))
        
    def __getattr__(self, k):
        try:
            return getattr(self.tr, k)
        except AttributeError:
            try:
                return getattr(self.bb, k)
            except AttributeError:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{k}")
        
        