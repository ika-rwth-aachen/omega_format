from datetime import datetime

import numpy as np
from h5py import Group, File
from ._version import get_versions
from .reference_resolving import InputClassBase
from .settings import get_settings
import parse


def get_converter_version(h5file, group_str):
    if group_str in h5file and 'converterVersion' in h5file.get(group_str).attrs:
        return MetaData.assure_string(h5file[group_str].attrs['converterVersion'])
    else:
        return None


class MetaData(InputClassBase):
    daytime: datetime = None
    format_version: str = get_versions()['version']
    recorder_number: int = None
    recording_number: int = None

    reference_point_lat: float = None
    reference_point_lon: float = None

    natural_behavior: bool = False
    natural_exposure: bool = False

    top_level_converter_version: str = None
    road_user_converter_version: str = None
    road_converter_version: str = None
    weather_converter_version: str = None
    state_converter_version: str = None
    misc_object_converter_version: str = None

    custom_information: str = ""
    reference_modality: int = None

    @property
    def version_identifier(self):
        none2string = lambda x: "0.0" if x is None else x
        return (f'C({none2string(self.top_level_converter_version)})' +
                f'U({none2string(self.road_user_converter_version)})' +
                f'R({none2string(self.road_converter_version)})' +
                f'W({none2string(self.weather_converter_version)})' +
                f'S({none2string(self.state_converter_version)})' +
                f'M({none2string(self.misc_object_converter_version)})'
                )

    @classmethod
    def is_version_higher(cls, m1, m2):
        parsed = lambda x: parse.search('C({:d}.{:d})' +
                                        'U({:d}.{:d})' +
                                        'R({:d}.{:d})' +
                                        'W({:d}.{:d})' +
                                        'S({:d}.{:d})' +
                                        'M({:d}.{:d})', x).fixed
        m1 = parsed(m1)
        m2 = parsed(m2)
        if np.any(np.greater(m1, m2)) and np.all(np.greater_equal(m1, m2)):
            return True
        elif np.all(np.less_equal(m1, m2)):
            return False
        else:
            raise ValueError('Some subversions are higher and some are lower. This is not supported.')

    @staticmethod
    def get_attribute(file: File, name: str, dtype=None):
        value = file.attrs.get(name) if get_settings().ALLOW_INCOMPLETE_META_DATA else file.attrs[name]
        if value is not None and dtype is not None:
            return dtype(value)
        else:
            return value

    @classmethod
    def from_hdf5(cls, file: File, validate: bool = True):
        dt = cls.get_attribute(file, 'daytime')
        func = cls if validate else cls.construct
        self = func(
            daytime=datetime.strptime(cls.assure_string(dt), '%Y-%m-%dT%H:%M:%S.%f%z') if dt is not None else None,
            recorder_number=cls.get_attribute(file, 'recorderNumber', int),
            recording_number=cls.get_attribute(file, 'recordingNumber', int),
            reference_point_lat=cls.get_attribute(file, 'refPointLat', float),
            reference_point_lon=cls.get_attribute(file, 'refPointLong', float),
            natural_behavior=cls.get_attribute(file, 'naturalBehavior', bool),
            natural_exposure=cls.get_attribute(file, 'naturalExposure', bool),
            format_version=cls.assure_string(cls.get_attribute(file, 'formatVersion')),
            top_level_converter_version=cls.get_attribute(file, 'converterVersion'),
            road_user_converter_version=get_converter_version(file, "roadUser"),
            road_converter_version=get_converter_version(file, "road"),
            weather_converter_version=get_converter_version(file, "weather"),
            state_converter_version=get_converter_version(file, "state"),
            misc_object_converter_version=get_converter_version(file, "miscObject"),
            custom_information=cls.get_attribute(file, 'customInformation'),
            reference_modality=cls.get_attribute(file, 'referenceModality'),
        )
        return self

    def to_dict(self):
        output: dict = dict()
        # TODO do we need this?
        return output

    @classmethod
    def write_converter_version(cls, top_group: Group, sub_group: Group, version):
        if version is not None:
            top_group.require_group(sub_group).attrs.create('converterVersion', data=version)

    def to_hdf5(self, group: Group):
        group.attrs.create("daytime", data=datetime.strftime(self.daytime, '%Y-%m-%dT%H:%M:%S.%f%z')),
        group.attrs.create("recorderNumber", data=self.recorder_number)
        group.attrs.create("recordingNumber", data=self.recording_number)
        group.attrs.create("refPointLat", data=self.reference_point_lat)
        group.attrs.create("refPointLong", data=self.reference_point_lon)
        group.attrs.create("naturalBehavior", data=self.natural_behavior)
        group.attrs.create("naturalExposure", data=self.natural_exposure)
        group.attrs.create("formatVersion", data=self.format_version)
        if self.top_level_converter_version is not None:
            group.attrs.create("converterVersion", data=self.top_level_converter_version)

        self.write_converter_version(group, "roadUser", self.road_user_converter_version)
        self.write_converter_version(group, "road", self.road_converter_version)
        self.write_converter_version(group, "weather", self.weather_converter_version)
        self.write_converter_version(group, "state", self.state_converter_version)
        self.write_converter_version(group, "miscObject", self.misc_object_converter_version)

        group.attrs.create("customInformation", data=self.custom_information)
        group.attrs.create("referenceModality", data=self.reference_modality)

    @classmethod
    def assure_string(cls, byte_array):
        if type(byte_array) == bytes:
            return byte_array.decode("utf-8")
        else:
            return byte_array
