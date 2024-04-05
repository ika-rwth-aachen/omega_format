from h5py import Group
from pydantic.fields import Field

from ..enums import ReferenceTypes
from ..geometry import Polyline
from ..reference_resolving import ReferenceDict, InputClassBase, raise_not_resolved


class FlatMarking(InputClassBase):
    color: ReferenceTypes.FlatMarkingColor
    polyline: Polyline
    type: ReferenceTypes.FlatMarkingType
    value: int
    overridden_by: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], FlatMarking))
    overrides: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], FlatMarking))
    condition: ReferenceTypes.FlatMarkingCondition = ReferenceTypes.FlatMarkingCondition.UNKNOWN
    layer_flag: ReferenceTypes.LayerFlag = ReferenceTypes.LayerFlag.PERMANENT_GENERAL

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            color=ReferenceTypes.FlatMarkingColor(group.attrs["color"]),
            condition=ReferenceTypes.FlatMarkingCondition(group.attrs["condition"]),
            type=ReferenceTypes.FlatMarkingType(group.attrs["type"]),
            value=group.attrs["value"].astype(int),
            layer_flag=ReferenceTypes.LayerFlag(group.attrs["layerFlag"]),
            polyline=Polyline.from_hdf5(group, validate=validate),
            overrides=ReferenceDict(group['overrides'], FlatMarking),
            overridden_by=ReferenceDict(group['overriddenBy'], FlatMarking)
        )
        return self

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        assert len(i) == 3
        return input_recording.roads[i[0]].lanes[i[1]].flat_markings[i[2]]

    def to_hdf5(self, group: Group):
        group.create_dataset('overriddenBy', data=self.overridden_by.reference)
        group.create_dataset('overrides', data=self.overrides.reference)
        group.attrs.create('color', data=self.color)
        group.attrs.create('condition', data=self.condition)
        group.attrs.create('layerFlag', data=self.layer_flag)
        group.attrs.create('type', data=self.type)
        group.attrs.create('value', data=self.value)
        self.polyline.to_hdf5(group)
