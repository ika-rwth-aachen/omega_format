from collections import UserDict
from pydantic import BaseModel
from pydantic.fields import Field
from pathlib import Path
from typing import Union

import h5py

from .perception.ego_position import EgoPosition
from .perception.meta_object import MetaObject
from .perception.misc_info import MiscInfo
from .perception.object import Object
from .perception.sensor import Sensor
from .timestamps import Timestamps
from .pydantic_utils.pydantic_config import PydanticConfig


class PerceptionRecording(BaseModel):
    """
    Class that represents the OMEGA-PerceptionDB-Format in an object-oriented manner.
    """
    class Config(PydanticConfig):
        pass
    format_version: str = "1.3"
    converter_version: str = ""
    recorder_number: int = 0
    recording_number: int = 0
    ego_id: int = 0
    ego_offset: float = 0.
    custom_information: str = ""

    timestamps: Timestamps = Field(default_factory=Timestamps)
    meta_object: MetaObject = Field(default_factory=MetaObject)
    objects: UserDict = Field(default_factory=UserDict)
    sensors: UserDict = Field(default_factory=UserDict)
    misc_objects: UserDict = Field(default_factory=UserDict)
    ego_position: EgoPosition = Field(default_factory=EgoPosition)

    @classmethod
    def from_hdf5(cls, filename: Union[str, Path], validate: bool = True):
        if Path(filename).is_file():
            with h5py.File(filename, 'r') as file:
                func = cls if validate else cls.construct
                tfunc = Timestamps if validate else Timestamps.construct
                self = func(
                    format_version=file.attrs['formatVersion'],
                    converter_version=file.attrs['converterVersion'],
                    recorder_number=file.attrs['recorderNumber'],
                    recording_number=file.attrs['recordingNumber'],
                    ego_id=int(file.attrs['egoID']),
                    ego_offset=file.attrs['egoOffset'],
                    custom_information=file.attrs['customInformation'],
                    timestamps=tfunc(val=file['timestamps'][()]),
                    meta_object=MetaObject.from_hdf5(file['object'], validate=validate),
                    ego_position=EgoPosition.from_hdf5(file['egoPosition'], validate=validate),
                    sensors=UserDict({int(i): Sensor.from_hdf5(group, validate=validate) for i, group in file['sensor'].items()}),
                    misc_objects=UserDict({int(i): MiscInfo.from_hdf5(group, validate=validate) for i, group in file['miscInfo'].items()}),
                    objects=UserDict({int(i): Object.from_hdf5(group, validate=validate) for i, group in file['object'].items()}),
                )
                return self
        else:
            raise FileNotFoundError("File {} not found".format(filename))

    def to_hdf5(self, filename):
        with h5py.File(filename, 'w') as file:
            file.attrs.create('formatVersion', data=self.format_version)
            file.attrs.create('converterVersion', data=self.converter_version)
            file.attrs.create('recorderNumber', data=self.recorder_number)
            file.attrs.create('recordingNumber', data=self.recording_number)
            file.attrs.create('egoID', data=self.ego_id)
            file.attrs.create('egoOffset', data=self.ego_offset)
            file.attrs.create('customInformation', data=self.custom_information)

            file.create_dataset('timestamps', data=self.timestamps.val)

            self.ego_position.to_hdf5(file.create_group('egoPosition'))

            object_group = file.create_group('object')
            self.meta_object.to_hdf5(object_group)
            for id, obj in self.objects.items():
                obj.to_hdf5(object_group.create_group(str(id)))

            sensor_group = file.create_group('sensor')
            for id, sensor in self.sensors.items():
                sensor.to_hdf5(sensor_group.create_group(str(id)))

            misc_object_group = file.create_group('miscInfo')
            for id, miscObject in self.misc_objects.items():
                miscObject.to_hdf5(misc_object_group.create_group(str(id)))
