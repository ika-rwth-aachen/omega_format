import io
from collections import UserDict
from pathlib import Path
from typing import Union

import h5py
import numpy as np
import pydantic_numpy.typing as pnd
from pydantic.fields import Field

from .perception.ego_position import EgoPosition
from .perception.meta_object import MetaObject
from .perception.misc_info import MiscInfo
from .perception.object import Object
from .perception.sensor import Sensor
from .reference_resolving import InputClassBase
from .settings import get_settings


class PerceptionRecording(InputClassBase):
    """
    Class that represents the OMEGA-PerceptionDB-Format in an object-oriented manner.
    """
    format_version: str = "1.3"
    converter_version: str = ""
    recorder_number: str = ""
    recording_number: str = ""
    ego_id: str = "RU-1"
    ego_offset: float = 0.
    custom_information: str = ""

    timestamps: pnd.NpNDArray = Field(default_factory=np.array)
    meta_object: MetaObject = Field(default_factory=MetaObject)
    objects: UserDict = Field(default_factory=UserDict)
    sensors: UserDict = Field(default_factory=UserDict)
    misc_objects: UserDict = Field(default_factory=UserDict)
    ego_position: EgoPosition = Field(default_factory=EgoPosition)

    @classmethod
    def from_hdf5(cls, filename: Union[str, Path, io.BytesIO], validate: bool = True, legacy=None):
        if isinstance(filename, io.BytesIO) or Path(filename).is_file():
            with h5py.File(filename, 'r') as file:
                func = cls if validate else cls.model_construct
                self = func(
                    format_version=file.attrs['formatVersion'],
                    converter_version=file.attrs['converterVersion'],
                    recorder_number=file.attrs['recorderNumber'],
                    recording_number=file.attrs['recordingNumber'],
                    ego_id=file.attrs['egoID'],
                    ego_offset=file.attrs['egoOffset'],
                    custom_information=file.attrs['customInformation'],
                    timestamps=file['timestamps'][()],
                    meta_object=MetaObject.from_hdf5(file['object'], validate=validate),
                    ego_position=EgoPosition.from_hdf5(file['egoPosition'], validate=validate),
                    sensors=UserDict({int(i): Sensor.from_hdf5(group, validate=validate) for i, group in file['sensor'].items()}),
                    misc_objects=UserDict({int(i): MiscInfo.from_hdf5(group, validate=validate) for i, group in file['miscInfo'].items()}),
                    objects=UserDict({i: Object.from_hdf5(group, validate=validate) for i, group in file['object'].items()}),
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

            file.create_dataset('timestamps', data=self.timestamps, **get_settings().hdf5_compress_args)

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
