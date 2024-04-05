from ..enums import ReferenceTypes
from ..settings import DefaultValues
from ..road import Boundary, Lane, Border, Sign, FlatMarking, LateralMarking
from ..dynamics import RoadUser, BoundingBox, Trajectory
from ..perception import Object
from typing import List
import random
import pyqtgraph as pg

from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsSimpleTextItem, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsItemGroup
from PyQt5.QtGui import QPen, QBrush, QColor, QTransform, QPainterPath, QPolygonF
from PyQt5.QtCore import QPointF

import numpy as np

__all__ = ['color_random', 'polyline2d', 'polygon2d', 'get_pen', 'get_random_pen', 'get_random_brush', 'get_brush',
           'bbx2d', 'bbx2d_text', 'visualize_objects', 'visualize_perc_object', 'visualize_perc_trajectory']


def polyline2d(tuples: List[tuple], pen: QPen = None, brush: QBrush = None, tooltip: str = None, text: str = None):
    points = [QPointF(x, y) for x, y in tuples]
    path = QPainterPath(points[0])
    for p in points[1:]:
        path.lineTo(p)
    path = QGraphicsPathItem(path)
    if pen:
        path.setPen(pen)
    if text:
        text_item = QGraphicsSimpleTextItem(text, path)
        text_item.setBrush(brush)
        font = text_item.font()
        font.setPointSize(4)
        text_item.setFont(font)

        center_point = points[0]
        direction_vector = points[0] - points[1]
        if direction_vector.x() == 0 and direction_vector.y() == 0 and len(points) > 2:
            direction_vector = points[1] - points[2]

        heading = np.rad2deg(-np.arctan2(direction_vector.y(), direction_vector.x()))

        text_item.setPos(center_point)
        text_item.setTransformOriginPoint(center_point)

        transform = QTransform()
        transform.scale(0.1, -0.1)
        transform.rotate(heading + 180)
        text_item.setTransform(transform)

        if tooltip:
            info_point = center_point
            box = bbx2d(info_point.x(), info_point.y(), 0.1, 0.1, heading, tooltip, pen)
            box.setParentItem(path)

    return path


def polygon2d(tuples: List[tuple], pen: QPen = None, brush: QBrush = None, text: str = None):
    points = [QPointF(x, y) for x, y in tuples]
    poly = QGraphicsPolygonItem(QPolygonF(points))
    poly.setPen(pen)
    poly.setBrush(brush)
    if text:
        text_item = QGraphicsSimpleTextItem(text, poly)
        font = text_item.font()
        font.setPointSize(4)
        text_item.setFont(font)
        text_item.setBrush(QBrush(QColor(255, 255, 255, brush.color().alpha())))

        transform = QTransform()
        transform.scale(0.1, -0.1)
        text_item.setTransform(transform)
        text_item.setPos(poly.boundingRect().center())

    return poly


def get_pen(color: tuple, width: float = .1):
    pen = QPen(QColor(*color))
    pen.setWidthF(width)
    return pen


def get_brush(color: tuple):
    return QBrush(QColor(*color))


def get_random_brush(alpha: int = 120):
    return QBrush(color_random(alpha))


def color_random(alpha: int = 120):
    return QColor(random.randint(10, 255), random.randint(10, 255), random.randint(10, 255), alpha)


def get_random_pen(width: float = .1, alpha: int = 120):
    pen = QPen(color_random(alpha))
    pen.setWidthF(width)
    return pen


def bbx2d(x: float, y: float, length: float, width: float, heading: float, text: str = None, pen: QPen = None,
          brush: QBrush = None):
    """
    Draws bounding box with the given parameters
    """
    # bounding box
    rectangle_outer = QGraphicsRectItem(x - length / 2, y - width / 2, length, width)
    arrow = QGraphicsPolygonItem(QPolygonF([QPointF(a, b) for a, b in [
        [x, y - width / 2],
        [x, y + width / 2],
        [x + length / 2, y]]]))
    rectangle = QGraphicsItemGroup()
    rectangle.addToGroup(rectangle_outer)
    rectangle.addToGroup(arrow)

    if pen:
        rectangle_outer.setPen(pen)
        arrow.setPen(pen)
    if brush:
        rectangle_outer.setBrush(brush)
        arrow.setBrush(brush)
    center_point = rectangle.boundingRect().center()
    trans_rot = QTransform()
    trans_rot.translate(center_point.x(), center_point.y())
    trans_rot.rotate(heading)
    trans_rot.translate(-center_point.x(), -center_point.y())
    rectangle.setTransform(trans_rot)
    rectangle.setToolTip(text)
    return rectangle


def bbx2d_text(x: float, y: float, length: float, width: float, heading: float, text: str, color: str):
    text_item = QGraphicsSimpleTextItem()
    font = text_item.font()
    font.setPointSize(2)
    text_item.setFont(font)
    text_item.setBrush(QBrush(pg.mkColor(color)))

    text_item.setText(text)

    text_bounding_translate = QTransform()
    text_bounding_translate.translate(width, -0.2 * width)
    text_bounding_translate.scale(0.1, -0.1)

    text_translate = QTransform()
    text_translate.translate(x, y)

    text_item.setTransform(text_bounding_translate * text_translate)

    return text_item


def visualize_objects(input_recording, index: tuple, cls, text: str = '', tooltip: str = '', pen: str = '#000000',
                      brush: str = '#000000', timestamp: int = 0):
    if cls == 'centerline':
        obj = Lane.resolve_func(input_recording, index)
        return visualize_lane(input_recording, index, obj, text, tooltip, pen, brush)
    else:
        obj = cls.resolve_func(input_recording, index)
        if cls == Border:
            return visualize_border(input_recording, index, obj, text, tooltip, pen, brush)
        elif cls == Boundary:
            return visualize_boundary(input_recording, index, obj, text, tooltip, pen, brush)
        elif cls == Lane:
            return visualize_lane(input_recording, index, obj, text, tooltip, pen, brush)
        elif cls == LateralMarking:
            return visualize_lateral_marking(input_recording, index, obj, text, tooltip, pen, brush)
        elif cls == FlatMarking:
            return visualize_flat_marking(input_recording, index, obj, text, tooltip, pen, brush)
        elif cls == Sign:
            return visualize_sign(input_recording, index, obj, text, tooltip, pen, brush)
        elif cls == RoadUser:
            return visualize_traffic_participant(input_recording, index, obj, text, tooltip, pen, brush, timestamp)
        elif cls == Trajectory:
            return visualize_trajectory(input_recording, index, obj, text, tooltip, pen, brush, timestamp)
        else:
            raise TypeError(f"Visualization for class {cls} not implemented!")


def visualize_border(input_recording, index: tuple, border, text: str = '', tooltip: str = '', pen: str = '#000000',
                     brush: str = '#000000'):
    return polyline2d(zip(border.polyline.pos_x, border.polyline.pos_y), pen, brush, text=text)


def visualize_boundary(input_recording, index: tuple, boundary, text: str = '', tooltip: str = '', pen: str = '#000000',
                       brush: str = '#000000'):
    lane = Lane.resolve_func(input_recording, (index[0], index[1]))
    if boundary.is_right_boundary:
        poly = lane.border_right.value.polyline
    else:
        poly = lane.border_left.value.polyline
    all_points = list(zip(poly.pos_x, poly.pos_y))
    start = boundary.poly_index_start
    end = boundary.poly_index_end
    is_reverse = end < start
    if is_reverse:
        start = end
        end = boundary.poly_index_start
    points = all_points[start:end + 1]
    if is_reverse:
        points = list(reversed(points))
    return polyline2d(points, pen=pen, brush=brush, text=text, tooltip=tooltip)


def visualize_lane(input_recording, index: tuple, lane, text: str = '', tooltip: str = '', pen: str = '#000000',
                   brush: str = '#000000'):
    return polygon2d(lane.polygon(), pen, brush, text=text)


def visualize_lateral_marking(input_recording, index: tuple, lateral_marking, text='', tooltip='', pen='#000000',
                              brush='#000000'):
    poly = lateral_marking.polyline
    points = list(zip(poly.pos_x, poly.pos_y))
    return polyline2d(points, pen=pen, brush=brush, text=text, tooltip=tooltip)


def visualize_flat_marking(input_recording, index: tuple, lateral_marking, text='', tooltip='', pen='#000000',
                           brush='#000000'):
    poly = lateral_marking.polyline
    points = list(zip(poly.pos_x, poly.pos_y))
    return polyline2d(points, pen=pen, brush=brush, text=text, tooltip=tooltip)


def visualize_sign(input_recording, index: tuple, sign, text: str = '', tooltip: str = '', pen: str = '#000000',
                   brush: str = '#000000'):
    poly = sign.position
    point = QPointF(poly.pos_x, poly.pos_y)

    return bbx2d(point.x(), point.y(), sign.length, sign.width, np.rad2deg(sign.heading), tooltip, pen, brush)


def visualize_center_line(input_recording, index: tuple, lane, text: str = '', tooltip: str = '', pen: str = '#000000',
                          brush: str = '#000000'):
    return polyline2d(lane.centerline.coords, pen, brush)


def visualize_traffic_participant(input_recording, index: tuple, tp, text: str = '', tooltip: str = '',
                                  pen: str = '#000000', brush: str = '#000000', timestamp: int = 0):
    # different visualization for ego vehicle
    def tp_items(tp, text, timestamp, pen, brush, color):
        index = timestamp - tp.birth
        x = tp.tr.pos_x[index]
        y = tp.tr.pos_y[index]

        if tp.bb.length == 0 or tp.bb.width == 0:
            if tp.type is ReferenceTypes.RoadUserType.PEDESTRIAN:
                tp.bb = BoundingBox()
                tp.bb.vec = DefaultValues.pedestrian
            elif tp.type is ReferenceTypes.RoadUserType.BICYCLE:
                tp.bb = BoundingBox()
                tp.bb.vec = DefaultValues.bicycle

        length = tp.bb.length
        width = tp.bb.width
        heading = tp.tr.heading[index]

        bbx = bbx2d(x, y, length, width, heading, text, pen, brush)
        bbx_text = bbx2d_text(x, y, length, width, heading, text, color)
        return bbx, bbx_text

    color = '#0000ff' if tp is input_recording.ego_vehicle else '#ff0000'

    return tp_items(tp, text, timestamp, pen, brush, color)


def visualize_perc_object(snip, index: tuple, obj, text: str = '', tooltip: str = '', pen: str = '#000000',
                          brush: str = '#000000', timestamp: int = 0):
    def obj_items(obj: Object, text, timestamp, pen, brush, color):
        index = timestamp - obj.birth_stamp

        x = obj.dist_lateral.val[index]
        y = obj.dist_longitudinal.val[index]

        length = obj.length.val[index]
        width = obj.width.val[index]
        heading = obj.heading.val[index]

        bbx = bbx2d(x, y, length, width, heading, text, pen, brush)
        bbx_text = bbx2d_text(x, y, length, width, heading, text, color)
        return bbx, bbx_text

    color = '#ffffff'

    return obj_items(obj, text, timestamp, pen, brush, color)


def visualize_trajectory(input_recording, index: tuple, tr, text: str = '', tooltip: str = '', pen: str = '#000000',
                         brush: str = '#000000', timestamp: int = 0):
    tp = RoadUser.resolve_func(input_recording, index)

    try:
        comet_tail_length = int(text)
    except Exception:
        comet_tail_length = 40
    idx = timestamp - tp.birth
    x_list = tr.pos_x[np.max([0, idx - comet_tail_length]):idx + 1]
    y_list = tr.pos_y[np.max([0, idx - comet_tail_length]):idx + 1]

    path = polyline2d(zip(x_list, y_list), pen=pen)
    return path


def visualize_perc_trajectory(input_recording, index: tuple, obj, text: str = '', tooltip: str = '',
                              pen: str = '#000000', brush: str = '#000000', timestamp: int = 0):
    try:
        comet_tail_length = int(text)
    except Exception:
        comet_tail_length = 40
    idx = timestamp - obj.birth_stamp
    x_list = obj.dist_lateral.val[np.max([0, idx - comet_tail_length]):idx + 1]
    y_list = obj.dist_longitudinal.val[np.max([0, idx - comet_tail_length]):idx + 1]

    path = polyline2d(zip(x_list, y_list), pen=pen)
    return path
