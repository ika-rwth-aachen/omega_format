from pydantic.types import conint, confloat
from pydantic.fields import Field
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase, ReferenceDict, raise_not_resolved


class Boundary(InputClassBase):
    color: ReferenceTypes.BoundaryColor = None
    condition: ReferenceTypes.BoundaryCondition = None
    poly_index_start: conint(ge=0) = 0
    poly_index_end: conint(ge=0) = 0
    type: ReferenceTypes.BoundaryType = None
    sub_type: ReferenceTypes.BoundarySubType = None
    is_right_boundary: bool  = None
    overridden_by: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Boundary))
    overrides: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Boundary))
    height: confloat(ge=0) = 0
    layer_flag: ReferenceTypes.LayerFlag = ReferenceTypes.LayerFlag.PERMANENT_GENERAL

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = cls(
            color=ReferenceTypes.BoundaryColor(group.attrs["color"]),
            condition=ReferenceTypes.BoundaryCondition(group.attrs["condition"]),
            poly_index_start=group.attrs["polyIndexStart"],
            poly_index_end=group.attrs["polyIndexEnd"],
            type=ReferenceTypes.BoundaryType(group.attrs["type"]),
            sub_type=ReferenceTypes.BoundarySubType(group.attrs["subtype"]),
            is_right_boundary=group.attrs["right"].astype(bool),
            height=group.attrs["height"],
            layer_flag=ReferenceTypes.LayerFlag(group.attrs["layerFlag"]),
            overrides=ReferenceDict(group['overrides'], Boundary),
            overridden_by=ReferenceDict(group['overriddenBy'], Boundary)
        )
        return self

    def to_dict(self):
        output: dict = dict()
        output["type"] = ReferenceTypes.BoundaryType(self.type).name
        output["is_right_boundary"] = self.is_right_boundary
        output["height"] = self.height
        output["sub_type"] = self.sub_type
        output["color"] = ReferenceTypes.BoundaryColor(self.color).name
        output["condition"] = ReferenceTypes.BoundaryCondition(self.condition).name
        output["overridden_by"] = self.overridden_by
        output["overrides"] = self.overrides
        output["layer_flag"] = self.layer_flag
        output["poly_index_start"] = self.poly_index_start
        output["poly_index_end"] = self.poly_index_end
        return output

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        assert len(i) == 3
        return input_recording.roads[i[0]].lanes[i[1]].boundaries[i[2]]

    def to_hdf5(self, group: Group):
        group.attrs.create('color', data=self.color)
        group.attrs.create('condition', data=self.condition)
        group.attrs.create('height', data=self.height)
        group.attrs.create('layerFlag', data=self.layer_flag)
        group.attrs.create('polyIndexStart', data=self.poly_index_start)
        group.attrs.create('polyIndexEnd', data=self.poly_index_end)
        group.attrs.create('type', data=self.type)
        group.attrs.create('subtype', data=self.sub_type)
        group.attrs.create('right', data=self.is_right_boundary)
        group.create_dataset('overriddenBy', data=self.overridden_by.reference)
        group.create_dataset('overrides', data=self.overrides.reference)
