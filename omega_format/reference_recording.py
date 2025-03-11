import io
import sys
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from itertools import chain
from pathlib import Path
from typing import List, Optional, Union
import h5py
import numpy as np
import pydantic_numpy.typing as pnd
from pydantic.dataclasses import Field
from tqdm import tqdm

from .dynamics.misc_object import MiscObject
from .dynamics.road_user import RoadUser
from .enums import ReferenceTypes
from .meta_data import MetaData
from .reference_resolving import (
    DictWithProperties,
    InputClassBase,
    ListWithProperties,
    require_group,
)
from .road.road import Road
from .road.state import State
from .settings import get_settings
from .weather.weather import Weather


def is_road_user(obj):
    return 'is_data_recorder' in obj.attrs or 'isDataRecorder' in obj.attrs
def is_misc_object(obj):
    return 'is_data_recorder' not in obj.attrs and 'isDataRecorder' not in obj.attrs

class ReferenceRecording(InputClassBase):
    """
    Class that represents the OMEGAFormat Reference Recording in an object-oriented manner.
    """
    meta_data: MetaData = Field(default_factory=MetaData)
    timestamps: pnd.NpNDArray = Field(default_factory=np.array)
    ego_id: Optional[str] = None
    ego_vehicle: Optional[RoadUser] = None
    weather: Optional[Weather] = None
    misc_objects: DictWithProperties[str, MiscObject] = Field(default_factory=DictWithProperties)
    roads: DictWithProperties[str, Road] = Field(default_factory=DictWithProperties)
    states: DictWithProperties[str, State] = Field(default_factory=DictWithProperties)
    road_users: DictWithProperties[str, RoadUser] = Field(default_factory=DictWithProperties)


    @property 
    def dynamic_objects(self):
        return {k: v for d in [self.misc_objects, self.road_users] for k,v in d.items()}

    @classmethod
    def from_hdf5(cls, filename: Union[str, Path, io.BytesIO], validate: bool = True, legacy=None):
        if isinstance(filename, io.BytesIO) or Path(filename).is_file():
            with h5py.File(filename, 'r') as file:
                func = cls if validate else cls.model_construct
                if legacy is None and file.attrs['formatVersion'] in ['v3.1', 'v3.0']:
                    legacy='v3.1'
                if legacy=='v3.1':
                    self = func(
                        roads=Road.convert2objects(file, "road", True, validate=validate, legacy=legacy),
                        states=State.convert2objects(file, "state", True, validate=validate, legacy=legacy),
                        misc_objects=DictWithProperties({f'M{k}': v for k, v in MiscObject.convert2objects(file, "miscObject", True, validate=validate, legacy=legacy).items()}),
                        road_users=DictWithProperties({f'RU{k}': v for k,v in RoadUser.convert2objects(file, "roadUser", True, validate=validate, legacy=legacy).items()}),
                        weather=Weather.from_hdf5(file['weather'], validate=validate, legacy=legacy) if require_group(file, "weather") else None,
                        timestamps=file['timestamps'][:] if require_group(file, "timestamps") else np.array([]),
                        meta_data=MetaData.from_hdf5(file, validate=validate, legacy=legacy)
                    )
                elif legacy is not None:
                    raise NotImplementedError()
                else:
                    self = func(
                        roads=Road.convert2objects(file, "road", True, validate=validate),
                        states=State.convert2objects(file, "state", True, validate=validate),
                        weather=Weather.from_hdf5(file['weather'], validate=validate) if require_group(file, "weather") else None,
                        timestamps=file['timestamps'][:] if require_group(file, "timestamps") else np.array([]),
                        meta_data=MetaData.from_hdf5(file, validate=validate),
                        misc_objects=DictWithProperties({k: MiscObject.from_hdf5(o, validate=validate, legacy=legacy) for k, o in file.get('dynamicObjects', {}).items() if is_misc_object(o)}),
                        road_users=DictWithProperties({k: RoadUser.from_hdf5(o, validate=validate, legacy=legacy) for k, o in file.get('dynamicObjects', {}).items() if is_road_user(o)})
                    )

                self.ego_id = cls.extract_ego_id(road_users=self.road_users)
                if self.ego_id is not None and self.ego_vehicle is None:
                    self.ego_vehicle = self.road_users.pop(self.ego_id)
                self.resolve()
                return self

        else:
            raise FileNotFoundError("File {} not found".format(filename))

    @classmethod
    def extract_ego_id(cls, road_users):
        data_recorders = [k for k, v in road_users.items() if v.is_data_recorder]
        if len(data_recorders) == 1:
            ego_id = data_recorders[0]
            return ego_id
        elif len(data_recorders) > 1:
            raise ValueError('Only one data recorder is allowed')

    def to_hdf5(self, filename):
        self.resolve()
        with h5py.File(filename, 'w') as f:
            self.meta_data.to_hdf5(f)

            f.create_dataset('timestamps', data=self.timestamps, **get_settings().hdf5_compress_args)

            self.road_users.to_hdf5(f.require_group('dynamicObjects'))
            if self.ego_vehicle is not None:
                ig = f['dynamicObjects'].create_group(str(self.ego_id))
                self.ego_vehicle.to_hdf5(ig)
            self.misc_objects.to_hdf5(f.require_group('dynamicObjects'))
            
            self.roads.to_hdf5(f.require_group('road'))
            self.states.to_hdf5(f.require_group('state'))

            if self.weather is not None:
                self.weather.to_hdf5(f.require_group('weather'))

    def resolve(self, input_recording=None):
        self.set_timestamps()
        #self.set_polys()
        for kr, r in self.roads.items():
            r.idx = kr
            for lr, l in r.lanes.items():
                l.idx = (kr, lr)
                l.road = r
        super().resolve(input_recording=self)

    def set_polys(self):
        for r in self.road_users.values():
            if r.polygon is None:
                r._set_corners_and_polygon()
        for m in self.misc_objects.values():
            if m.polygon is None:
                m._set_corners_and_polygon()
                
    def set_timestamps(self):
        for r in self.road_users.values():
            r._set_timestamps(self)
        for m in self.misc_objects.values():
            m._set_timestamps(self)

    @property
    def movable_objects(self):
        return ListWithProperties(chain.from_iterable([self.road_users.values(), self.misc_objects.values()]))

    @property
    def movable_objects_with_ego(self):
        return ListWithProperties(chain.from_iterable([self.road_users.values(),
                                                       self.misc_objects.values(),
                                                       ([self.ego_vehicle] if self.ego_vehicle is not None else [])]))

    @property
    def road_objects(self):
        return ListWithProperties(chain.from_iterable([r.road_objects.values() for r in self.roads.values()]))

    @property
    def signs(self):
        return ListWithProperties(chain.from_iterable([r.signs.values() for r in self.roads.values()]))

    @property
    def structural_objects(self):
        return ListWithProperties(chain.from_iterable([r.structural_objects.values() for r in self.roads.values()]))

    def cut_to_timespan(self, birth, death, inplace=True):
        """Mutates the object itself: Cuts all Objects in structure to the given timespan."""
        if not inplace:
            self = deepcopy(self)
        for prop in [getattr(self, o) for o in dir(self) if not o.startswith('_') if not callable(getattr(self,o)) and hasattr(getattr(self,o), 'cut_to_timespan')]:
            try:
                prop.cut_to_timespan(birth, death)
            except AttributeError:
                pass
        self.timestamps = self.timestamps[birth:death+1]
        self.resolve()
        return self

    def extract_snippet(self, tp_id):
        if tp_id == self.ego_id:
            return deepcopy(self)
        
        assert tp_id in self.road_users
        assert self.road_users[tp_id].type == ReferenceTypes.RoadUserType.CAR

        ir = deepcopy(self)
        if ir.ego_vehicle is not None:
            ir.road_users[ir.ego_id] = ir.ego_vehicle
            ir.ego_id = ir.ego_vehicle = None
        birth = ir.road_users[tp_id].birth
        death = ir.road_users[tp_id].end
        ir.ego_vehicle = ir.road_users[tp_id]
        ir.ego_id = tp_id
        del ir.road_users[tp_id]
        ir.ego_vehicle.original_birth = birth
        ir.cut_to_timespan(birth, death)
        ir.ego_vehicle.is_data_recorder = True

        return ir

    def extract_snippets(self, max_snippets=None, ids=None):
        """
        Produces list of `ReferenceRecordings` with exactly one ego vehicle.
        If one data recorder is marked in the input, then only this one becomes the ego vehicle.
        If no data recorder is marked in the input, then each car is the ego vehicle once.
        :param max_snippets: set -1 for extracting snippets for all cars
        :return: list(InputRecording)
        """
        if ids is None:
            ids = self.get_snippet_tp_ids(max_snippets=max_snippets)

        with ThreadPoolExecutor(max_workers=8) as executor:
            snippets = executor.map(self.extract_snippet, tqdm(ids, desc='Extract individual snippets', unit='snippet', file=sys.stdout, leave=False, position=1))
        return list(snippets)


    def compress_ir_to_snippets(self, ids: List[int]):
        """
        cuts the input_recording to the length
        """
        start = np.inf
        end = -np.inf
        for i in ids:
            start = np.min([start, self.road_users[i].birth])
            end = np.max([end, self.road_users[i].end])
        self.cut_to_timespan(int(start), int(end))
        return self

    def get_snippet_tp_ids(self, max_snippets=None, ignore_ego=False):
        if ignore_ego or self.ego_id is None:
            ids = [k for k, v in self.road_users.items() if v.type == ReferenceTypes.RoadUserType.CAR and not np.all(v.tr.is_static)]
            if max_snippets is not None and max_snippets != 0 and max_snippets != -1:
                ids = ids[:max_snippets]
        else:
            ids = [self.ego_id]
        return ids
