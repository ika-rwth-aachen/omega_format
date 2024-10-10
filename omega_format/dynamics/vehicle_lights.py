from pydantic.fields import Field
from typing import List
from h5py import Group
from ..enums import ReferenceTypes
from ..reference_resolving import InputClassBase
from ..settings import get_settings


def map_lights(group, s):
    return list(map(ReferenceTypes.RoadUserVehicleLights, group[s][:].tolist()))

class VehicleLights(InputClassBase):
    indicator_right: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    indicator_left: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    brake_lights: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    headlights: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    reverseing_lights: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    blue_light: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)
    orange_light: List[ReferenceTypes.RoadUserVehicleLights] = Field(default_factory=list)

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            indicator_right=map_lights(group, 'indicatorRight'),
            indicator_left=map_lights(group, 'indicatorLeft'),
            brake_lights=map_lights(group, 'brakeLights'),
            headlights=map_lights(group, 'headlights'),
            reverseing_lights=map_lights(group, 'reversingLights'),
            blue_light=map_lights(group, 'blueLight'),
            **({} if legacy=='v3.1' else {'orange_light': map_lights(group, 'orangeLight')})
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('indicatorRight', data=self.indicator_right, **get_settings().hdf5_compress_args)
        group.create_dataset('indicatorLeft', data=self.indicator_left, **get_settings().hdf5_compress_args)
        group.create_dataset('brakeLights', data=self.brake_lights, **get_settings().hdf5_compress_args)
        group.create_dataset('headlights', data=self.headlights, **get_settings().hdf5_compress_args)
        group.create_dataset('reversingLights', data=self.reverseing_lights, **get_settings().hdf5_compress_args)
        group.create_dataset('blueLight', data=self.blue_light, **get_settings().hdf5_compress_args)
        group.create_dataset('orangeLight', data=self.orange_light, **get_settings().hdf5_compress_args)