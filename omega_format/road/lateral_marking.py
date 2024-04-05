from pydantic.fields import Field
from h5py import Group

from .lane import Lane
from ..enums import ReferenceTypes
from ..geometry import Polyline
from ..reference_resolving import InputClassBase, ReferenceDict, raise_not_resolved
from typing_extensions import Annotated


class LateralMarking(InputClassBase):
    type: ReferenceTypes.LateralMarkingType
    polyline: Polyline
    long_size: Annotated[float, Field(ge=0)]
    color: ReferenceTypes.LateralMarkingColor
    applicable_lanes: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Lane))
    overridden_by: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], LateralMarking))
    overrides: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], LateralMarking))
    condition: ReferenceTypes.LateralMarkingCondition = ReferenceTypes.LateralMarkingCondition.UNKNOWN
    layer_flag: ReferenceTypes.LayerFlag = ReferenceTypes.LayerFlag.PERMANENT_GENERAL

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            type=ReferenceTypes.LateralMarkingType(group.attrs["type"]),
            polyline=Polyline.from_hdf5(group),
            long_size=group.attrs["longSize"].astype(float),
            color=ReferenceTypes.LateralMarkingColor(group.attrs["color"]),
            applicable_lanes=ReferenceDict(group['applicableLanes'][:], Lane),
            condition=ReferenceTypes.LateralMarkingCondition(group.attrs["condition"]),
            layer_flag=ReferenceTypes.LayerFlag(group.attrs["layerFlag"]),
            overrides=ReferenceDict(group['overrides'], LateralMarking),
            overridden_by=ReferenceDict(group['overriddenBy'], LateralMarking)
        )
        return self

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        assert len(i) == 2
        return input_recording.roads[i[0]].lateral_markings[i[1]]

    def to_hdf5(self, group: Group):
        group.create_dataset('applicableLanes', data=self.applicable_lanes.reference)
        group.create_dataset('overriddenBy', data=self.overridden_by.reference)
        group.create_dataset('overrides', data=self.overrides.reference)
        group.attrs.create('color', data=self.color)
        group.attrs.create('condition', data=self.condition)
        group.attrs.create('layerFlag', data=self.layer_flag)
        group.attrs.create('type', data=self.type)
        group.attrs.create('longSize', data=self.long_size)
        self.polyline.to_hdf5(group)
