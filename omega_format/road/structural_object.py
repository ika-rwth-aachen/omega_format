from pydantic.fields import Field

from h5py import Group

from ..enums import ReferenceTypes
from ..geometry import Polyline
from ..reference_resolving import ReferenceDict, InputClassBase
from typing_extensions import Annotated


class StructuralObject(InputClassBase):
    type: ReferenceTypes.StructuralObjectType
    polyline: Polyline
    overridden_by: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], StructuralObject))
    overrides: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], StructuralObject))
    height: Annotated[float, Field(ge=0)] = 0
    layer_flag: ReferenceTypes.LayerFlag = ReferenceTypes.LayerFlag.PERMANENT_GENERAL

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            type=ReferenceTypes.StructuralObjectType(group.attrs["type"]),
            polyline=Polyline.from_hdf5(group),
            height=group.attrs["height"].astype(float),
            layer_flag=ReferenceTypes.LayerFlag(group.attrs["layerFlag"]),
            overrides=ReferenceDict(group['overrides'], StructuralObject),
            overridden_by=ReferenceDict(group['overriddenBy'], StructuralObject)
        )
        return self

    def to_hdf5(self, group: Group):
        group.attrs.create('height', data=self.height)
        group.attrs.create('layerFlag', data=self.layer_flag)
        group.attrs.create('type', data=self.type)
        group.create_dataset('overriddenBy', data=self.overridden_by.reference)
        group.create_dataset('overrides', data=self.overrides.reference)
        self.polyline.to_hdf5(group)
