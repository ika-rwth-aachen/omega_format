from typing import Optional

import numpy as np
import shapely
from h5py import Group
from pydantic.fields import Field

from ..enums import ReferenceTypes
from ..reference_resolving import (
    DictWithProperties,
    InputClassBase,
    ReferenceDict,
    ReferenceElement,
    raise_not_resolved,
)
from .border import Border
from .boundary import Boundary
from .flat_marking import FlatMarking
from .surface import Surface


class Lane(InputClassBase):
    border_right: Optional[ReferenceElement] = None
    border_left: Optional[ReferenceElement] = None
    type: Optional[ReferenceTypes.LaneType] = ReferenceTypes.LaneType.UNKNOWN
    subtype: Optional[ReferenceTypes.LaneSubType] = ReferenceTypes.LaneSubType.UNKNOWN
    boundaries: DictWithProperties = Field(default_factory=DictWithProperties)
    predecessors: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Lane))
    successors: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Lane))
    border_right_is_inverted: bool = False
    border_left_is_inverted: bool = False
    flat_markings: DictWithProperties = Field(default_factory=DictWithProperties)
    surface: Surface = Field(default_factory=Surface)
    classification: ReferenceTypes.LaneClass = ReferenceTypes.LaneClass.NONE
    layer_flag: bool = False

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            border_right=ReferenceElement(group['borderRight'][:], Border),
            border_left=ReferenceElement(group['borderLeft'][:], Border),
            type=ReferenceTypes.LaneType(group.attrs["type"]),
            subtype=ReferenceTypes.LaneSubType(group.attrs["subtype"]),
            boundaries=Boundary.convert2objects(group, 'boundary', validate=validate),
            predecessors=ReferenceDict(group['predecessor'], Lane),
            successors=ReferenceDict(group['successor'], Lane),
            border_right_is_inverted=group.attrs["invertedRight"].astype(bool),
            border_left_is_inverted=group.attrs["invertedLeft"].astype(bool),
            flat_markings=FlatMarking.convert2objects(group, 'flatMarking', validate=validate),
            surface=Surface.from_hdf5(group['surface'], validate=validate),
            classification=ReferenceTypes.LaneClass(group.attrs["class"]),
            layer_flag=group.attrs["layerFlag"].astype(bool),
        )
        return self

    def to_dict(self):
        output: dict = dict()
        output["type"] = ReferenceTypes.LaneType(self.type).name
        output["subtype"] = ReferenceTypes.LaneSubType(self.subtype).name
        output["border_right"] = self.border_left.reference
        output["border_left"] = self.border_right.reference
        boundaries_dict = dict()
        for bid, boundary in self.boundaries.items():
            boundaries_dict[f'{bid}'] = boundary.to_dict()
        output["boundaries"] = boundaries_dict

        return output

    def oriented_borders(self):
        rb_min = np.inf
        rb_max = 0
        lb_min = np.inf
        lb_max = 0
        for b in self.boundaries.values():
            if b.is_right_boundary:
                rb_min = int(np.min(np.array([rb_min, b.poly_index_start, b.poly_index_end])))
                rb_max = int(np.max(np.array([rb_max, b.poly_index_start, b.poly_index_end])))
            else:
                lb_min = int(np.min(np.array([lb_min, b.poly_index_start, b.poly_index_end])))
                lb_max = int(np.max(np.array([lb_max, b.poly_index_start, b.poly_index_end])))

        lb = list(zip(self.border_left.value.polyline.pos_x, self.border_left.value.polyline.pos_y))
        lb = lb[lb_min:lb_max + 1]
        if self.border_left_is_inverted:
            lb = list(reversed(lb))
        rb = list(zip(self.border_right.value.polyline.pos_x, self.border_right.value.polyline.pos_y))
        rb = rb[rb_min:rb_max + 1]
        if self.border_right_is_inverted:
            rb = list(reversed(rb))
        return lb, rb

    def start_points(self):
        lb, rb = self.oriented_borders()
        return [lb[0], rb[0]]

    def end_points(self):
        lb, rb = self.oriented_borders()
        return [lb[-1], rb[-1]]

    def get_polygon(self):
        lb, rb = self.oriented_borders()
        rb = list(reversed(rb))
        return lb + rb

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        assert len(i) == 2
        return input_recording.roads[i[0]].lanes[i[1]]

    def to_hdf5(self, group: Group):
        group.attrs.create('class', data=self.classification)
        group.attrs.create('type', data=self.type if self.type is not None else ReferenceTypes.LaneType.UNKNOWN)
        group.attrs.create('subtype', data=int(self.subtype if self.subtype is not None else ReferenceTypes.LaneSubType.UNKNOWN))
        group.create_dataset('borderRight', data=self.border_right.reference)
        group.create_dataset('borderLeft', data=self.border_left.reference)
        group.attrs.create('invertedLeft', data=self.border_left_is_inverted)
        group.attrs.create('invertedRight', data=self.border_right_is_inverted)
        group.create_dataset('predecessor', data=self.predecessors.reference)
        group.create_dataset('successor', data=self.successors.reference)
        group.attrs.create('layerFlag', data=self.layer_flag)
        self.boundaries.to_hdf5(group.create_group('boundary'))
        self.surface.to_hdf5(group.create_group('surface'))

        flat_marking_group = group.create_group('flatMarking')
        for id, flat_marking in self.flat_markings.items():
            flat_marking.to_hdf5(flat_marking_group.create_group(str(id)))

    @property
    def sub_type(self):
        return self.subtype
    
    @sub_type.setter
    def sub_type(self, v):
        self.subtype = v
        
    @property
    def polygon(self):
        polygon = shapely.geometry.Polygon([(x, y) for x, y in self.get_polygon()])
        if not polygon.is_valid:
            lb, rb = self.oriented_borders()
            polygon = shapely.geometry.Polygon(np.array(lb + list(reversed(rb))))
            if not polygon.is_valid:
                polygon = polygon.convex_hull
        return polygon