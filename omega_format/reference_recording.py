import sys
from copy import deepcopy
from pydantic.dataclasses import Field
from itertools import chain
from pathlib import Path
from typing import Optional, Union, List

import h5py
import numpy as np
from tqdm import tqdm

from .dynamics.road_user import RoadUser
from .dynamics.misc_object import MiscObject
from .enums import ReferenceTypes
from .meta_data import MetaData
from .reference_resolving import InputClassBase, DictWithProperties, ListWithProperties, require_group
from .road.road import Road
from .road.state import State
from .timestamps import Timestamps
from .weather.weather import Weather
from concurrent.futures import ThreadPoolExecutor

class ReferenceRecording(InputClassBase):
    """
    Class that represents the OMEGA Format Reference Recording in an object-oriented manner.
    """
    meta_data: MetaData = Field(default_factory=MetaData)
    timestamps: Timestamps = Field(default_factory=Timestamps)
    ego_id: Optional[int] = None
    ego_vehicle: Optional[RoadUser] = None
    weather: Weather = None
    misc_objects: DictWithProperties = Field(default_factory=DictWithProperties)
    roads: DictWithProperties = Field(default_factory=DictWithProperties)
    states: DictWithProperties = Field(default_factory=DictWithProperties)
    road_users: DictWithProperties = Field(default_factory=DictWithProperties)

    @classmethod
    def from_hdf5(cls, filename: Union[str, Path], validate: bool = True):

        if Path(filename).is_file():
            with h5py.File(filename, 'r') as file:
                func = cls if validate else cls.construct
                tfunc = Timestamps if validate else Timestamps.construct
                self = func(
                    misc_objects=MiscObject.convert2objects(file, "miscObject", True, validate=validate),
                    roads=Road.convert2objects(file, "road", True, validate=validate),
                    states=State.convert2objects(file, "state", True, validate=validate),
                    road_users=RoadUser.convert2objects(file, "roadUser", True, validate=validate),
                    weather=Weather.from_hdf5(file['weather'], validate=validate) if require_group(file, "weather") else None,
                    timestamps=tfunc(val=file['timestamps'][:]) if require_group(file, "timestamps") else Timestamps(),
                    meta_data=MetaData.from_hdf5(file, validate=validate)
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
        with h5py.File(filename, 'w') as f:
            self.meta_data.to_hdf5(f)

            f.create_dataset('timestamps', data=self.timestamps.val)

            self.road_users.to_hdf5(f.require_group('roadUser'))
            if self.ego_vehicle is not None:
                ig = f['roadUser'].create_group(str(self.ego_id))
                self.ego_vehicle.to_hdf5(ig)
            self.misc_objects.to_hdf5(f.require_group('miscObject'))
            self.roads.to_hdf5(f.require_group('road'))
            self.states.to_hdf5(f.require_group('state'))

            if self.weather is not None:
                self.weather.to_hdf5(f.require_group('weather'))

    def resolve(self, input_recording=None):
        super().resolve(input_recording=self)

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

    def cut_to_timespan(self, birth, death):
        """Mutates the object itself: Cuts all Objects in structure to the given timespan."""
        for prop in [p for p in [getattr(self,o) for o in dir(self) if not o.startswith('_')] if not callable(p) and not isinstance(p, ListWithProperties)]:
            try:
                prop.cut_to_timespan(birth, death)
            except AttributeError as e:
                pass
        self.resolve()

    def extract_snippet(self, tp_id):
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
            if max_snippets is not None or max_snippets == 0 or max_snippets == -1:
                ids = ids[:max_snippets]
        else:
            ids = [self.ego_id]
        return ids
