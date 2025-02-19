from pydantic.fields import Field

from .dynamic_object import DynamicObject
from .vehicle_lights import VehicleLights
from ..enums import ReferenceTypes
from ..reference_resolving import raise_not_resolved, ReferenceElement, ReferenceNotResolved
from .trajectory import Trajectory
from .bounding_box import BoundingBox

from h5py import Group


class RoadUser(DynamicObject):
    type: ReferenceTypes.RoadUserType
    subtype: ReferenceTypes.RoadUserSubType = ReferenceTypes.RoadUserSubTypeGeneral.REGULAR
    is_data_recorder: bool = False
    vehicle_lights: VehicleLights = Field(default_factory=VehicleLights)
    id: str = 'RU-1'

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        if legacy=='v3.1':
            return cls._legacy_from_hdf5_v3_1(group, validate, legacy=legacy)
        elif legacy is None:
            classification_type = ReferenceTypes.RoadUserType(group.attrs["type"])
            sub_group_name = group.name.rpartition('/')[-1]
            func = cls if validate else cls.model_construct
            self = func(
                id=sub_group_name,
                type=classification_type,
                subtype=ReferenceTypes.RoadUserType.get_subtype(classification_type, group.attrs["subtype"]),
                connected_to=ReferenceElement(id=group.attrs["connectedTo"], object_class=DynamicObject),
                attached_to=ReferenceElement(id=group.attrs["attachedTo"], object_class=DynamicObject),
                is_data_recorder=group.attrs["isDataRecorder"].astype(bool),
                birth=group.attrs["birthStamp"].astype(int),
                tr=Trajectory.from_hdf5(group['trajectory'], validate=validate),
                bb=BoundingBox.from_hdf5(group['boundBox'], validate=validate),
                vehicle_lights=VehicleLights.from_hdf5(group['vehicleLights'], validate=validate)
            )
            return self
        else:
            raise NotImplementedError()
        
        
    @classmethod
    def _legacy_from_hdf5_v3_1(cls, group: Group, validate: bool = True, legacy=None):
        classification_type = ReferenceTypes.RoadUserType(group.attrs["type"])
        sub_group_name = group.name.rpartition('/')[-1]
        func = cls if validate else cls.model_construct
        self = func(
            id=f'RU{sub_group_name}',
            type=classification_type,
            subtype=ReferenceTypes.RoadUserType.get_subtype(classification_type, group.attrs["subtype"]),
            connected_to=ReferenceElement(id=f'RU{group.attrs["connectedTo"]}', object_class=DynamicObject),
            is_data_recorder=group.attrs["isDataRecorder"].astype(bool),
            birth=group.attrs["birthStamp"].astype(int),
            tr=Trajectory.from_hdf5(group['trajectory'], validate=validate, legacy=legacy),
            bb=BoundingBox.from_hdf5(group['boundBox'], validate=validate, legacy=legacy),
            vehicle_lights=VehicleLights.from_hdf5(group['vehicleLights'], validate=validate, legacy=legacy)
        )
        return self

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        if i == input_recording.ego_id:
            if input_recording.ego_vehicle is None:
                raise ReferenceNotResolved()
            return input_recording.ego_vehicle
        else:
            return input_recording.road_users[i]

    def to_hdf5(self, group: Group):
        super().to_hdf5(group)
        group.attrs.create('isDataRecorder', data=self.is_data_recorder)
        group.attrs.create('type', data=self.type)
        group.attrs.create('subtype', data=self.subtype)
        self.vehicle_lights.to_hdf5(group.create_group('vehicleLights'))

    @property
    def sub_type(self):
        return self.subtype
    
    @sub_type.setter
    def sub_type(self, v):
        self.subtype = v