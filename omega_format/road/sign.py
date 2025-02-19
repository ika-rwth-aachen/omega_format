import warnings
from h5py import Group
from pydantic.dataclasses import Field

from .lane import Lane
from .state import State
from ..settings import DefaultValues
from ..enums import ReferenceTypes
from ..geometry import Position
from ..reference_resolving import ReferenceDict, InputClassBase, raise_not_resolved
from typing_extensions import Annotated
from typing import Optional

class Sign(InputClassBase):
    type: ReferenceTypes.SignType
    value: int
    history: str
    applicable_lanes: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Lane))
    position: Position
    heading: float
    size_class: int
    size: Annotated[float, Field(ge=0)] = 1.0
    overridden_by: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Sign))
    overrides: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Sign))
    connected_to: ReferenceDict = Field(default_factory=lambda: ReferenceDict([], Sign))
    state: Optional[State] = None
    layer_flag: ReferenceTypes.LayerFlag = ReferenceTypes.LayerFlag.PERMANENT_GENERAL
    fallback: bool = False
    weather_dependent: bool = False
    time_dependent: bool = False

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        type_ = group.attrs["type"]
        if isinstance(type_, bytes):
            type_ = type_.decode("utf-8")
        try:
            type_ = ReferenceTypes.SignType(type_)
        except ValueError:
            warn_text = f'[Sign type {type_} not found in `enums/reference_types.py` and is interpreted as {ReferenceTypes.SignType.UNKNOWN.name}'
            warnings.warn(warn_text)
            type_ = ReferenceTypes.SignType.UNKNOWN

        func = cls if validate else cls.model_construct
        self = func(
            type=type_,
            value=group.attrs["value"].astype(int),
            size_class=group.attrs["sizeClass"].astype(int),
            history=group.attrs["history"],
            time_dependent=group.attrs["timedependent"].astype(bool),
            weather_dependent=group.attrs["weatherdependent"].astype(bool),
            applicable_lanes=ReferenceDict(group['applicableLanes'], Lane),
            connected_to=ReferenceDict(group['connectedTo'], Sign),
            fallback=group.attrs["fallback"].astype(bool),
            position=Position.from_hdf5(group, validate=validate),
            heading=group.attrs["heading"].astype(float),
            layer_flag=ReferenceTypes.LayerFlag(group.attrs["layerFlag"]),
            overrides=ReferenceDict(group['overrides'], Sign),
            overridden_by=ReferenceDict(group['overriddenBy'], Sign)
        )
        return self

    @property
    def length(self):
        return DefaultValues.sign[0]

    @property
    def width(self):
        return DefaultValues.sign[1]

    @classmethod
    @raise_not_resolved
    def resolve_func(cls, input_recording, i):
        assert len(i) == 2
        return input_recording.roads[i[0]].signs[i[1]]

    def to_hdf5(self, group: Group):
        group.create_dataset('applicableLanes', data=self.applicable_lanes.reference)
        group.create_dataset('connectedTo', data=self.connected_to.reference)
        group.attrs.create('fallback', data=self.fallback)
        group.attrs.create('heading', data=self.heading)
        group.attrs.create('history', data=self.history)
        group.attrs.create('layerFlag', data=self.layer_flag)
        group.create_dataset('overriddenBy', data=self.overridden_by.reference)
        group.create_dataset('overrides', data=self.overrides.reference)
        group.attrs.create('sizeClass', data=self.size_class)
        group.attrs.create('timedependent', data=self.time_dependent)
        group.attrs.create('type', data=self.type.encode('utf-8'))
        group.attrs.create('value', data=self.value)
        group.attrs.create('weatherdependent', data=self.weather_dependent)
        self.position.to_hdf5(group)
