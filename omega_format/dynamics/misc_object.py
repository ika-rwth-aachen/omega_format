from h5py import Group
from pydantic.fields import Field

from .dynamic_object import DynamicObject
from ..enums import ReferenceTypes
from ..reference_resolving import *
from .trajectory import Trajectory
from .bounding_box import BoundingBox


class MiscObject(DynamicObject):
    type: ReferenceTypes.MiscObjectType = Field(default_factory=ReferenceTypes.MiscObjectType)
    sub_type: ReferenceTypes.MiscObjectSubType = Field(default_factory=ReferenceTypes.MiscObjectSubType)
    id: str = f'M-1'

    @classmethod
    def from_hdf5(cls, group: Group, validate=True, legacy=None):
        if legacy=='v3.1':
            return cls._legacy_from_hdf5_v3_1(group, validate=validate)
        elif legacy is None:
            sub_group_name = group.name.rpartition('/')[-1]
            func = cls if validate else cls.construct
            self = func(
                id=sub_group_name,
                tr=Trajectory.from_hdf5(group['trajectory'], validate=validate),
                bb=BoundingBox.from_hdf5(group['boundBox'], validate=validate),
                connected_to=ReferenceElement(id=group.attrs["connectedTo"], object_class=DynamicObject),
                attached_to=ReferenceElement(id=group.attrs["attachedTo"], object_class=DynamicObject),
                type=ReferenceTypes.MiscObjectType(group.attrs["type"]),
                sub_type=ReferenceTypes.MiscObjectSubType(group.attrs["subtype"]),
                birth=group.attrs["birthStamp"].astype(int)
            )
            return self
        else:
            raise NotImplementedError()

    @classmethod
    def _legacy_from_hdf5_v3_1(cls, group: Group, validate=True):
        sub_group_name = group.name.rpartition('/')[-1]
        func = cls if validate else cls.construct
        self = func(
            id=f'M{sub_group_name}',
            tr=Trajectory.from_hdf5(group['trajectory'], validate=validate),
            bb=BoundingBox.from_hdf5(group['boundBox'], validate=validate),
            type=ReferenceTypes.MiscObjectType(group.attrs["type"]),
            sub_type=ReferenceTypes.MiscObjectSubType(group.attrs["subtype"]),
            birth=group.attrs["birthStamp"].astype(int)
        )
        return self

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        return input_recording.misc_objects[i]

    def to_hdf5(self, group: Group):
        super().to_hdf5(group)
        group.create_dataset('type', data=self.type)
        group.create_dataset('subtype', data=self.sub_type)
