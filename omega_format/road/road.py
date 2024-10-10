from pydantic.dataclasses import Field
from h5py import Group

from .border import Border
from .lane import Lane
from .lateral_marking import LateralMarking
from .road_object import RoadObject
from .sign import Sign
from .structural_object import StructuralObject
from ..enums import ReferenceTypes
from ..reference_resolving import DictWithProperties, raise_not_resolved, InputClassBase
from typing import Optional

class Road(InputClassBase):
    location: Optional[ReferenceTypes.RoadLocation] = None
    lateral_markings: DictWithProperties = Field(default_factory=DictWithProperties)
    lanes: DictWithProperties = Field(default_factory=DictWithProperties)
    borders: DictWithProperties = Field(default_factory=DictWithProperties)
    road_objects: DictWithProperties = Field(default_factory=DictWithProperties)
    signs: DictWithProperties = Field(default_factory=DictWithProperties)
    structural_objects: DictWithProperties = Field(default_factory=DictWithProperties)

    @property
    def num_lanes(self):
        return len(self.lanes)

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        assert len(i) == 1
        return input_recording.roads[i]

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            location=ReferenceTypes.RoadLocation(group.attrs["location"]),
            lateral_markings=LateralMarking.convert2objects(group, 'lateralMarking', validate=validate),
            lanes=Lane.convert2objects(group, 'lane', validate=validate),
            borders=Border.convert2objects(group, 'border', validate=validate),
            road_objects=RoadObject.convert2objects(group, 'roadObject', validate=validate),
            structural_objects=StructuralObject.convert2objects(group, 'structuralObject', validate=validate),
            signs=Sign.convert2objects(group, 'sign', validate=validate)
        )
        return self

    def to_hdf5(self, group: Group):
        group.attrs.create('location', data=self.location)
        group.attrs.create('numLanes', data=self.num_lanes)
        self.borders.to_hdf5(group.create_group('border'))
        self.lanes.to_hdf5(group.create_group('lane'))
        self.lateral_markings.to_hdf5(group.create_group('lateralMarking'))
        self.road_objects.to_hdf5(group.create_group('roadObject'))
        self.signs.to_hdf5(group.create_group('sign'))
        self.structural_objects.to_hdf5(group.create_group('structuralObject'))
