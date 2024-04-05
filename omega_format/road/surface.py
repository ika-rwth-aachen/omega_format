from pydantic.fields import Field
from h5py import Group

from ..enums import ReferenceTypes
from ..reference_resolving import ReferenceDict, InputClassBase


class Surface(InputClassBase):
    overridden_by: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Surface))
    overrides: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Surface))
    color: ReferenceTypes.SurfaceColor = ReferenceTypes.SurfaceColor.UNKNOWN
    condition: ReferenceTypes.SurfaceCondition = ReferenceTypes.SurfaceCondition.NO_VALUE
    material: ReferenceTypes.SurfaceMaterial = ReferenceTypes.SurfaceMaterial.UNKNOWN
    layer_flag: ReferenceTypes.LayerFlag = ReferenceTypes.LayerFlag.PERMANENT_GENERAL

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            material=ReferenceTypes.SurfaceMaterial(group.attrs["material"]),
            color=ReferenceTypes.SurfaceColor(group.attrs["color"]),
            condition=ReferenceTypes.SurfaceCondition(group.attrs["condition"]),
            layer_flag=ReferenceTypes.LayerFlag(group.attrs["layerFlag"]),
            overrides=ReferenceDict(group['overrides'], Surface),
            overridden_by=ReferenceDict(group['overriddenBy'], Surface)
        )
        return self

    def to_hdf5(self, group: Group):
        group.attrs.create('condition', data=self.condition)
        group.attrs.create('color', data=self.color)
        group.attrs.create('layerFlag', data=self.layer_flag)
        group.attrs.create('material', data=self.material)
        group.create_dataset('overriddenBy', data=self.overridden_by.reference)
        group.create_dataset('overrides', data=self.overrides.reference)
