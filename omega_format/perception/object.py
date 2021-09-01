from typing import List
from warnings import warn

import numpy as np
from h5py import Group
from pydantic import validator, BaseModel
from pydantic.fields import Field

from .valvar import ValVar
from ..enums import PerceptionTypes
from ..pydantic_utils.pydantic_config import PydanticConfig


class ObjectClassification(BaseModel):
    class Config(PydanticConfig):
        pass
    val: List[PerceptionTypes.ObjectClassification] = Field(default_factory=list)
    confidence: np.ndarray = np.array([], dtype=np.float64)

    @validator('confidence')
    def check_confidence_values(cls, v):
        for value in v:
            assert 0 <= value <= 1, f"confidence value should be between 0 and 1, but is {value}"
        return v

    @validator('confidence')
    def check_array_length(cls, v, values):
        if len(v) != len(values.get('val')):
            warn('length of confidence array does not match array length for classification. This is only possible if confidence is of type not_provided')
        # assert len(v) == len(values.get('val')), f"length of confidence array does not match classifications array"
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = func(
            val=list(map(PerceptionTypes.ObjectClassification, group['val'][()].tolist())),
            confidence=group['confidence'][()],
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('val', data=self.val)
        group.create_dataset('confidence', data=self.confidence)

    def cut_to_timespan(self, birth, death):
        assert birth >= 0
        assert birth <= death

        if len(self.val) > 0:
            assert len(self.val) > birth
            assert len(self.val) > death
            self.val = self.val[birth:death + 1]

        if len(self.confidence) > 0:
            assert len(self.confidence) > birth
            assert len(self.confidence) > death
            self.confidence = self.confidence[birth:death + 1]

'''
class TrackingPoint(BaseModel):
    class Config(PydanticConfig):
        pass
    val: List[PerceptionTypes.TrackingPoint] = Field(default_factory=list)
    var: np.ndarray = np.array([], dtype=np.float64)

    @validator('val')
    def check_array_not_empty(cls, v):
        if not len(v) > 0:
            warn('received empty array in TrackingPoint class')
        return v

    @validator('var')
    def check_array_length(cls, v, values):
        if len(values) > 0:
            # first array would be validated if len(values)=0 -> no length to compare against
            # use the length of pos_x to check equality with other array length
            length = len(values.get('val'))
            if len(v) != length:
                raise ValueError(f'length of all TrackingPoint arrays must match, expected len {len(v)}, actual len {length}')
        return v

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        func = cls if validate else cls.construct
        self = func(
            val=list(map(PerceptionTypes.TrackingPoint, group['val'][()].tolist())),
            var=group['var'][()],
        )
        return self

    def to_hdf5(self, group: Group):
        group.create_dataset('val', data=self.val)
        group.create_dataset('var', data=self.var)

    def cut_to_timespan(self, birth, death):
        assert birth >= 0
        assert birth <= death

        if len(self.val) > 0:
            assert len(self.val) > birth
            assert len(self.val) > death
            self.val = self.val[birth:death + 1]

        if len(self.var) > 0:
            assert len(self.var) > birth
            assert len(self.var) > death
            self.var = self.var[birth:death + 1]
'''

class Object(BaseModel):
    class Config(PydanticConfig):
        pass
    id: int = -1
    birth_stamp: int = 0

    heading: ValVar = Field(default_factory=ValVar)
    width: ValVar = Field(default_factory=ValVar)
    height: ValVar = Field(default_factory=ValVar)
    length: ValVar = Field(default_factory=ValVar)

    rcs: np.ndarray = np.array([])
    age: np.ndarray = np.array([])
    tracking_point: List[PerceptionTypes.TrackingPoint] = Field(default_factory=list)

    confidence_of_existence: np.ndarray = np.array([])
    movement_classification: List[PerceptionTypes.MovementClassification] = Field(default_factory=list)
    meas_state: List[PerceptionTypes.MeasState] = Field(default_factory=list)

    dist_longitudinal: ValVar = Field(default_factory=ValVar)
    dist_lateral: ValVar = Field(default_factory=ValVar)
    dist_z: ValVar = Field(default_factory=ValVar)
    rel_vel_longitudinal: ValVar = Field(default_factory=ValVar)
    rel_vel_lateral: ValVar = Field(default_factory=ValVar)
    abs_vel_longitudinal: ValVar = Field(default_factory=ValVar)
    abs_vel_lateral: ValVar = Field(default_factory=ValVar)
    rel_acc_longitudinal: ValVar = Field(default_factory=ValVar)
    rel_acc_lateral: ValVar = Field(default_factory=ValVar)
    abs_acc_longitudinal: ValVar = Field(default_factory=ValVar)
    abs_acc_lateral: ValVar = Field(default_factory=ValVar)
    object_classification: ObjectClassification = Field(default_factory=ObjectClassification)

    @property
    def len(self):
        return len(self.dist_lateral.val)

    @property
    def end(self):
        return self.birth_stamp + self.len

    def in_timespan(obj, birth, death):
        return birth < (obj.birth_stamp + len(obj.dist_lateral.val)) and death >= obj.birth_stamp

    def cut_to_timespan(self, birth, death):
        # local timespan of the object, not recording!
        assert birth >= 0
        assert birth <= death
        assert self.len > death

        self.birth_stamp += birth

        for k, v in vars(self).items():
            if isinstance(v, ValVar) or isinstance(v, ObjectClassification):
                v.cut_to_timespan(birth, death)
            elif isinstance(v, np.ndarray) or isinstance(v, list):
                setattr(self, k, v[birth:death + 1])

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True):
        sub_group_name = group.name.rpartition('/')[-1]
        func = cls if validate else cls.construct
        self = func(
            id=int(sub_group_name),
            birth_stamp=group.attrs['birthStamp'].astype(int),

            heading=ValVar.from_hdf5(group['heading'], validate=validate),
            width=ValVar.from_hdf5(group['width'], validate=validate),
            height=ValVar.from_hdf5(group['height'], validate=validate),
            length=ValVar.from_hdf5(group['length'], validate=validate),
            rcs=group['rcs'][()],
            age=group['age'][()],
            tracking_point=group['trackingPoint'][()],
            confidence_of_existence=group['confidenceOfExistence'][()],

            movement_classification=list(map(PerceptionTypes.MovementClassification,
                                             group['movementClassification'][()].tolist())),
            meas_state=list(map(PerceptionTypes.MeasState, group['measState'][()].tolist())),

            dist_longitudinal=ValVar.from_hdf5(group['distLongitudinal'], validate=validate),
            dist_lateral=ValVar.from_hdf5(group['distLateral'], validate=validate),
            dist_z=ValVar.from_hdf5(group['distZ'], validate=validate),
            rel_vel_longitudinal=ValVar.from_hdf5(group['relVelLongitudinal'], validate=validate),
            rel_vel_lateral=ValVar.from_hdf5(group['relVelLateral'], validate=validate),
            abs_vel_longitudinal=ValVar.from_hdf5(group['absVelLongitudinal'], validate=validate),
            abs_vel_lateral=ValVar.from_hdf5(group['absVelLateral'], validate=validate),
            rel_acc_longitudinal=ValVar.from_hdf5(group['relAccLongitudinal'], validate=validate),
            rel_acc_lateral=ValVar.from_hdf5(group['relAccLateral'], validate=validate),
            abs_acc_longitudinal=ValVar.from_hdf5(group['absAccLongitudinal'], validate=validate),
            abs_acc_lateral=ValVar.from_hdf5(group['absAccLateral'], validate=validate),
            object_classification=ObjectClassification.from_hdf5(group['objectClassification'], validate=validate),
        )
        return self

    def to_hdf5(self, group: Group):
        group.attrs.create('birthStamp', data=self.birth_stamp)

        self.heading.to_hdf5(group.create_group('heading'))
        self.width.to_hdf5(group.create_group('width'))
        self.height.to_hdf5(group.create_group('height'))
        self.length.to_hdf5(group.create_group('length'))
        group.create_dataset('rcs', data=self.rcs)
        group.create_dataset('age', data=self.age)
        group.create_dataset('trackingPoint', data=self.tracking_point)
        group.create_dataset('confidenceOfExistence', data=self.confidence_of_existence)
        group.create_dataset('movementClassification', data=self.movement_classification)
        group.create_dataset('measState', data=self.meas_state)

        self.dist_longitudinal.to_hdf5(group.create_group('distLongitudinal'))
        self.dist_lateral.to_hdf5(group.create_group('distLateral'))
        self.dist_z.to_hdf5(group.create_group('distZ'))
        self.rel_vel_longitudinal.to_hdf5(group.create_group('relVelLongitudinal'))
        self.rel_vel_lateral.to_hdf5(group.create_group('relVelLateral'))
        self.abs_vel_longitudinal.to_hdf5(group.create_group('absVelLongitudinal'))
        self.abs_vel_lateral.to_hdf5(group.create_group('absVelLateral'))
        self.rel_acc_longitudinal.to_hdf5(group.create_group('relAccLongitudinal'))
        self.rel_acc_lateral.to_hdf5(group.create_group('relAccLateral'))
        self.abs_acc_longitudinal.to_hdf5(group.create_group('absAccLongitudinal'))
        self.abs_acc_lateral.to_hdf5(group.create_group('absAccLateral'))
        self.object_classification.to_hdf5(group.create_group('objectClassification'))
