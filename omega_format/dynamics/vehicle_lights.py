from pydantic.fields import Field
from pydantic import BaseModel
from typing import List
from h5py import Group
from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..settings import get_settings

class VehicleLights(InputClassBase):
    indicator_right: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    indicator_left: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    brake_lights: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    headlights: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    reverseing_lights: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    blue_light: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        rf = lambda s: list(map(ReferenceTypes.RoadUserVehicleLights, group[s][:].tolist()))
        func = cls if validate else cls.construct
        self = func(
            indicator_right=rf('indicatorRight'),
            indicator_left=rf('indicatorLeft'),
            brake_lights=rf('brakeLights'),
            headlights=rf('headlights'),
            reverseing_lights=rf('reversingLights'),
            blue_light=rf('blueLight'),
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('indicatorRight', data=self.indicator_right, **get_settings().hdf5_compress_args)
        group.create_dataset('indicatorLeft', data=self.indicator_left, **get_settings().hdf5_compress_args)
        group.create_dataset('brakeLights', data=self.brake_lights, **get_settings().hdf5_compress_args)
        group.create_dataset('headlights', data=self.headlights, **get_settings().hdf5_compress_args)
        group.create_dataset('reversingLights', data=self.reverseing_lights, **get_settings().hdf5_compress_args)
        group.create_dataset('blueLight', data=self.blue_light, **get_settings().hdf5_compress_args)