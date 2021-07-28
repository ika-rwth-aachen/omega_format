from pydantic.fields import Field, Any

from .dynamic_object import DynamicObject
from .vehicle_lights import VehicleLights
from ..enums import ReferenceTypes
from ..reference_resolving import *
from .trajectory import Trajectory
from .bounding_box import BoundingBox

from h5py import Group


class RoadUser(DynamicObject):
    type: ReferenceTypes.RoadUserType = ReferenceTypes.RoadUserType.REGULAR
    sub_type: Any = None # ReferenceTypes.RoadUserSubType
    connected_to: ReferenceElement = None
    is_data_recorder: bool = False
    vehicle_lights: VehicleLights = Field(default_factory=VehicleLights)
    id: int = -1

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        classification_type = ReferenceTypes.RoadUserType(group.attrs["type"])
        sub_group_name = group.name.rpartition('/')[-1]
        func = cls if validate else cls.construct
        self = func(
            id=int(sub_group_name),
            type=classification_type,
            sub_type=ReferenceTypes.RoadUserType.get_subtype(classification_type, group.attrs["subtype"]),
            connected_to=ReferenceElement(id=group.attrs["connectedTo"], object_class=RoadUser),
            is_data_recorder=group.attrs["isDataRecorder"].astype(bool),
            birth=group.attrs["birthStamp"].astype(int),
            tr=Trajectory.from_hdf5(group['trajectory'], validate=validate),
            bb=BoundingBox.from_hdf5(group['boundBox'], validate=validate),
            vehicle_lights=VehicleLights.from_hdf5(group['vehicleLights'], validate=validate)
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
        group.attrs.create('birthStamp', data=self.birth)
        group.attrs.create('isDataRecorder', data=self.is_data_recorder)
        group.attrs.create('type', data=self.type)
        group.attrs.create('subtype', data=self.sub_type)
        if self.connected_to is not None:
            group.attrs.create('connectedTo', data=self.connected_to.reference)
        else:
            group.attrs.create('connectedTo', data=-1)
        self.bb.to_hdf5(group.create_group('boundBox'))
        self.tr.to_hdf5(group.create_group('trajectory'))
        self.vehicle_lights.to_hdf5(group.create_group('vehicleLights'))
