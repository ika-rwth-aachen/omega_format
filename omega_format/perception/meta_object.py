from h5py import Group

from ..enums import PerceptionTypes
from ..reference_resolving import InputClassBase


class MetaObject(InputClassBase):
    dist_longitudinal_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    dist_longitudinal_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    dist_lateral_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    dist_lateral_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    dist_z_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    dist_z_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    rel_vel_longitudinal_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    rel_vel_longitudinal_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    rel_vel_lateral_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    rel_vel_lateral_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    abs_vel_longitudinal_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    abs_vel_longitudinal_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    abs_vel_lateral_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    abs_vel_lateral_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    rel_acc_longitudinal_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    rel_acc_longitudinal_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    rel_acc_lateral_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    rel_acc_lateral_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    abs_acc_longitudinal_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    abs_acc_longitudinal_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    abs_acc_lateral_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    abs_acc_lateral_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    object_classification_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    object_classification_confidence_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED

    heading_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    heading_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    width_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    width_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    height_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    height_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    length_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    length_var_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    rcs_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    age_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    tracking_point_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    confidence_of_existence_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    movement_classification_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED
    meas_state_val_type: PerceptionTypes.PerceptionType = PerceptionTypes.PerceptionType.NOT_PROVIDED

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            dist_longitudinal_val_type=PerceptionTypes.PerceptionType(group.attrs['distLongitudinalValType']),
            dist_longitudinal_var_type=PerceptionTypes.PerceptionType(group.attrs['distLongitudinalVarType']),
            dist_lateral_val_type=PerceptionTypes.PerceptionType(group.attrs['distLateralValType']),
            dist_lateral_var_type=PerceptionTypes.PerceptionType(group.attrs['distLateralVarType']),
            dist_z_val_type=PerceptionTypes.PerceptionType(group.attrs['distZValType']),
            dist_z_var_type=PerceptionTypes.PerceptionType(group.attrs['distZVarType']),
            rel_vel_longitudinal_val_type=PerceptionTypes.PerceptionType(group.attrs['relVelLongitudinalValType']),
            rel_vel_longitudinal_var_type=PerceptionTypes.PerceptionType(group.attrs['relVelLongitudinalVarType']),
            rel_vel_lateral_val_type=PerceptionTypes.PerceptionType(group.attrs['relVelLateralValType']),
            rel_vel_lateral_var_type=PerceptionTypes.PerceptionType(group.attrs['relVelLateralVarType']),
            abs_vel_longitudinal_val_type=PerceptionTypes.PerceptionType(group.attrs['absVelLongitudinalValType']),
            abs_vel_longitudinal_var_type=PerceptionTypes.PerceptionType(group.attrs['absVelLongitudinalVarType']),
            abs_vel_lateral_val_type=PerceptionTypes.PerceptionType(group.attrs['absVelLateralValType']),
            abs_vel_lateral_var_type=PerceptionTypes.PerceptionType(group.attrs['absVelLateralVarType']),
            rel_acc_longitudinal_val_type=PerceptionTypes.PerceptionType(group.attrs['relAccLongitudinalValType']),
            rel_acc_longitudinal_var_type=PerceptionTypes.PerceptionType(group.attrs['relAccLongitudinalVarType']),
            rel_acc_lateral_val_type=PerceptionTypes.PerceptionType(group.attrs['relAccLateralValType']),
            rel_acc_lateral_var_type=PerceptionTypes.PerceptionType(group.attrs['relAccLateralVarType']),
            abs_acc_longitudinal_val_type=PerceptionTypes.PerceptionType(group.attrs['absAccLongitudinalValType']),
            abs_acc_longitudinal_var_type=PerceptionTypes.PerceptionType(group.attrs['absAccLongitudinalVarType']),
            abs_acc_lateral_val_type=PerceptionTypes.PerceptionType(group.attrs['absAccLateralValType']),
            abs_acc_lateral_var_type=PerceptionTypes.PerceptionType(group.attrs['absAccLateralVarType']),
            object_classification_val_type=PerceptionTypes.PerceptionType(group.attrs['objectClassificationValType']),
            object_classification_confidence_val_type=PerceptionTypes.PerceptionType(group.attrs['objectClassificationConfidenceValType']),

            heading_val_type=PerceptionTypes.PerceptionType(group.attrs['headingValType']),
            heading_var_type=PerceptionTypes.PerceptionType(group.attrs['headingVarType']),
            width_val_type=PerceptionTypes.PerceptionType(group.attrs['widthValType']),
            width_var_type=PerceptionTypes.PerceptionType(group.attrs['widthVarType']),
            height_val_type=PerceptionTypes.PerceptionType(group.attrs['heightValType']),
            height_var_type=PerceptionTypes.PerceptionType(group.attrs['heightVarType']),
            length_val_type=PerceptionTypes.PerceptionType(group.attrs['lengthValType']),
            length_var_type=PerceptionTypes.PerceptionType(group.attrs['lengthVarType']),
            rcs_val_type=PerceptionTypes.PerceptionType(group.attrs['rcsValType']),
            age_val_type=PerceptionTypes.PerceptionType(group.attrs['ageValType']),
            tracking_point_val_type=PerceptionTypes.PerceptionType(group.attrs['trackingPointValType']),
            confidence_of_existence_val_type=PerceptionTypes.PerceptionType(group.attrs['confidenceOfExistenceValType']),
            movement_classificaton_val_type=PerceptionTypes.PerceptionType(group.attrs['movementClassificationValType']),
            meas_state_val_type=PerceptionTypes.PerceptionType(group.attrs['measStateValType']),
        )
        return self

    def to_hdf5(self, group: Group):
        group.attrs.create('distLongitudinalValType', data=self.dist_longitudinal_val_type)
        group.attrs.create('distLongitudinalVarType', data=self.dist_longitudinal_var_type)
        group.attrs.create('distLateralValType', data=self.dist_lateral_val_type)
        group.attrs.create('distLateralVarType', data=self.dist_lateral_var_type)
        group.attrs.create('distZValType', data=self.dist_z_val_type)
        group.attrs.create('distZVarType', data=self.dist_z_var_type)
        group.attrs.create('relVelLongitudinalValType', data=self.rel_vel_longitudinal_val_type)
        group.attrs.create('relVelLongitudinalVarType', data=self.rel_vel_longitudinal_var_type)
        group.attrs.create('relVelLateralValType', data=self.rel_vel_lateral_val_type)
        group.attrs.create('relVelLateralVarType', data=self.rel_vel_lateral_var_type)
        group.attrs.create('absVelLongitudinalValType', data=self.abs_vel_longitudinal_val_type)
        group.attrs.create('absVelLongitudinalVarType', data=self.abs_vel_longitudinal_var_type)
        group.attrs.create('absVelLateralValType', data=self.abs_vel_lateral_val_type)
        group.attrs.create('absVelLateralVarType', data=self.abs_vel_lateral_var_type)
        group.attrs.create('relAccLongitudinalValType', data=self.rel_acc_longitudinal_val_type)
        group.attrs.create('relAccLongitudinalVarType', data=self.rel_acc_longitudinal_var_type)
        group.attrs.create('relAccLateralValType', data=self.rel_acc_lateral_val_type)
        group.attrs.create('relAccLateralVarType', data=self.rel_acc_lateral_var_type)
        group.attrs.create('absAccLongitudinalValType', data=self.abs_acc_longitudinal_val_type)
        group.attrs.create('absAccLongitudinalVarType', data=self.abs_acc_longitudinal_var_type)
        group.attrs.create('absAccLateralValType', data=self.abs_acc_lateral_val_type)
        group.attrs.create('absAccLateralVarType', data=self.abs_acc_lateral_var_type)
        group.attrs.create('objectClassificationValType', data=self.object_classification_val_type)
        group.attrs.create('objectClassificationConfidenceValType', data=self.object_classification_confidence_val_type)

        group.attrs.create('headingValType', data=self.heading_val_type)
        group.attrs.create('headingVarType', data=self.heading_var_type)
        group.attrs.create('widthValType', data=self.width_val_type)
        group.attrs.create('widthVarType', data=self.width_var_type)
        group.attrs.create('heightValType', data=self.height_val_type)
        group.attrs.create('heightVarType', data=self.height_var_type)
        group.attrs.create('lengthValType', data=self.length_val_type)
        group.attrs.create('lengthVarType', data=self.length_var_type)
        group.attrs.create('rcsValType', data=self.rcs_val_type)
        group.attrs.create('ageValType', data=self.age_val_type)
        group.attrs.create('trackingPointValType', data=self.tracking_point_val_type)
        group.attrs.create('confidenceOfExistenceValType', data=self.confidence_of_existence_val_type)
        group.attrs.create('movementClassificationValType', data=self.movement_classification_val_type)
        group.attrs.create('measStateValType', data=self.meas_state_val_type)
