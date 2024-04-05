import numpy as np
import pyqtgraph as pg

from .base import VisualizationModule
from ..pyqt_helper import get_pen, visualize_objects
from ...dynamics import Trajectory, RoadUser
from ...enums import ReferenceTypes

rut = ReferenceTypes.RoadUserType

def print_heading(snip, id_, index):
    tp = snip.reference.ego_vehicle if id_ == snip.reference.ego_id else snip.reference.road_users[id_]
    if hasattr(tp.tr, 'heading'):
        return f'\nheading:{tp.tr.heading[index]:.1f}'
    else:
        return ""

def print_speed(snip, id_, index):
    tp = snip.reference.ego_vehicle if id_ == snip.reference.ego_id else snip.reference.road_users[id_]
    if hasattr(tp.tr, 'vel_lateral') and hasattr(tp.tr, 'vel_longitudinal'):
        speed = np.sqrt(abs(tp.tr.vel_lateral[index])**2 + abs(tp.tr.vel_longitudinal[index])**2) * 3.6
        return f'\nspeed:{speed:.2f} km/h'
    else:
        return ""

class VisualizeTP(VisualizationModule):

    def __init__(self, text_funcs, **kwargs):
        super().__init__("Road User", **kwargs)
        self.text_funcs = text_funcs

    def _get_bounding_box_text(self, id_, index, snip):
        tp = snip.reference.ego_vehicle if id_ == snip.reference.ego_id else snip.reference.road_users[id_]
        text = f'{id_}:{tp.type.name}'
        if self.text_funcs is not None and len(self.text_funcs) > 0:
            text = f'{text}{"".join([func(snip, id_, index) for func in self.text_funcs])}'
        return text

    def visualize_dynamics(self, snip, timestamp, visualizer):
        items = []
        objects = {}
        objects.update(snip.reference.road_users)
        if snip.reference.ego_id is not None:
            objects[snip.reference.ego_id] = snip.reference.ego_vehicle
        if objects is not None:

            for id_, tp in objects.items():
                if hasattr(tp, 'in_timespan') and tp.in_timespan(timestamp, timestamp):
                    text = self._get_bounding_box_text(id_, timestamp-tp.birth, snip)

                    if tp is snip.reference.ego_vehicle:
                        # different visualization for ego vehicle
                        color = '#0000ff'
                        color_width = 3
                    elif tp.type in [rut.BICYCLE, rut.PEDESTRIAN, rut.PUSHABLE_PULLABLE, rut.WHEELCHAIR, rut.PERSONAL_MOBILITY_DEVICE]:
                        color = '#ff0000'
                        color_width = 3
                    else:
                        color = '#00ff00'
                        color_width = 2
                    pen = pg.mkPen(color, width=color_width)
                    brush = pg.mkBrush(color + '44')

                    bbx, bbx_text = visualize_objects(snip.reference, (id_), RoadUser, pen=pen, brush=brush,
                                                      text=text, timestamp=timestamp)

                    items.append(bbx)
                    items.append(bbx_text)

        return items


class VisualizeTPPath(VisualizationModule):
    def __init__(self, comet_tail_length_in_s=2, **kwargs):
        super().__init__('Road User Tail', **kwargs)
        self.comet_tail_length_in_s = comet_tail_length_in_s
        self.ego_pen = get_pen((0, 0, 255, 255))
        self.tp_pen = get_pen((0, 255, 0, 255))
        self.vru_pen = get_pen((255, 0, 0, 255))

    def visualize_dynamics(self, snip, timestamp, visualizer):
        """
        Visualizes the full paths of the objects
        """
        items = []

        objects = {k: v for k, v in snip.reference.road_users.items()}
        objects[snip.reference.ego_id] = snip.reference.ego_vehicle

        comet_tail_length = int(self.comet_tail_length_in_s * visualizer.fps)

        for id_, tp in objects.items():
            if hasattr(tp, 'in_timespan') and tp.in_timespan(timestamp, timestamp, ):
                if tp is snip.reference.ego_vehicle:
                    pen = self.ego_pen
                elif tp.type in [rut.BICYCLE, rut.PEDESTRIAN, rut.PUSHABLE_PULLABLE, rut.WHEELCHAIR, rut.PERSONAL_MOBILITY_DEVICE]:
                    pen = self.vru_pen
                else:
                    pen = self.tp_pen
                path = visualize_objects(snip.reference, (id_), Trajectory, pen=pen, timestamp=timestamp,
                                         text=comet_tail_length)  # TODO: add parameter instead of using text

                items.append(path)
        return items
