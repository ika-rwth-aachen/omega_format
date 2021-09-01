from enum import Enum, IntEnum


class PerceptionTypeSpecification(Enum):
    FORMAT_VERSION = 'v1.3'

class PerceptionType(IntEnum):
    NOT_PROVIDED = 0
    MEASURED = 1
    DETERMINED = 2


class SensorModality(IntEnum):
    LIDAR = 1
    CAMERA = 2
    RADAR_SR = 3
    RADAR_MR = 4
    RADAR_LR = 5
    FUSION = 6

class ObjectClassification(IntEnum):
    NO_INFO = 0
    CAR = 1
    TRUCK = 2
    MOTORCYCLE = 3
    PEDESTRIAN = 4
    BICYCLE = 5
    BIGGER_THAN_CAR = 11
    SMALLER_THAN_CAR = 12
    UNKNOWN_SMALL = 13
    UNKNOWN_BIG = 14
    UNKNOWN = 15

class MovementClassification(IntEnum):
    NO_INFO = 0
    UNKNOWN = 1
    MOVING = 2
    STATIONARY = 3
    ONCOMING = 4
    CROSSING_MOVING = 5
    CROSSING_STATIONARY = 6
    STOPPED = 7

class MeasState(IntEnum):
    UNKNOWN = 0
    DELETED = 1
    NEW_OBJECT = 2
    MEASURED = 3
    PREDICTED = 4
    DELETED_FROM_MERGE = 5
    NEW_FROM_MERGE = 6

class TrackingPoint(IntEnum):
    UNKNOWN = 0
    FRONT_RIGHT_CORNER = 1
    CENTER_OF_FRONT_EDGE = 2
    FRONT_LEFT_CORNER = 3
    CENTER_OF_LEFT_EDGE = 4
    CENTER_OF_VEHICLE = 5
    CENTER_OF_RIGHT_EDGE = 6
    REAR_LEFT_CORNER = 7
    CENTER_OF_REAR_EDGE = 8
    REAR_RIGHT_CORNER = 9
