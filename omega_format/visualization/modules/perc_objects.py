import numpy as np
import pyqtgraph as pg

from .base import VisualizationModule, SnippetContainer
from ..pyqt_helper import visualize_perc_object, visualize_perc_trajectory, get_pen
from ...perception import Object


def print_heading(obj: Object, index: int):
    return f'\nheading:{obj.heading.val[index]:.1f}'

def print_speed(obj: Object, index: int):
    speed = np.sqrt(abs(obj.abs_vel_lateral.val[index])**2 + abs(obj.abs_vel_longitudinal.val[index])**2) * 3.6
    return f'\nspeed:{speed:.2f} km/h'

class VisualizePerc(VisualizationModule):

    def __init__(self, text_funcs, **kwargs):
        super().__init__("Perception: Objects", **kwargs)
        self.requires = [SnippetContainer.REQ_PERCEPTION]
        self.text_funcs = text_funcs

    def get_bounding_box_text(self, id_, index: int, obj: Object):
        text = f'{id_}:{obj.object_classification.val[index].name}'
        if self.text_funcs is not None and len(self.text_funcs) > 0:
            text = f'{text}{"".join([func(obj, index) for func in self.text_funcs])}'
        return text


    def visualize_dynamics(self, snip, timestamp, visualizer):
        items = []

        for id_, obj in snip.perception.objects.items():  # type: int, Object
            if obj.in_timespan(timestamp, timestamp):
                text = self.get_bounding_box_text(id_, timestamp - obj.birth_stamp, obj)

                color = '#ffffff'
                color_width = 2
                pen = pg.mkPen(color, width=color_width)
                brush = pg.mkBrush(color + '44')

                bbx, bbx_text = visualize_perc_object(snip, id_, obj, text, pen=pen, brush=brush, timestamp=timestamp)

                items.append(bbx)
                items.append(bbx_text)

        return items


class VisualizePercPath(VisualizationModule):
    def __init__(self, comet_tail_length_in_s=2, **kwargs):
        super().__init__('Perception: Object Tail', **kwargs)
        self.requires = [SnippetContainer.REQ_PERCEPTION]
        self.comet_tail_length_in_s = comet_tail_length_in_s
        self.pen = get_pen((255, 255, 255, 255))


    def visualize_dynamics(self, snip, timestamp, visualizer):
        """
        Visualizes the full paths of the objects
        """
        items = []
        comet_tail_length = int(self.comet_tail_length_in_s * visualizer.fps)

        for id_, obj in snip.perception.objects.items():
            if obj.in_timespan(timestamp, timestamp):
                path = visualize_perc_trajectory(snip.perception, id_, obj, text=comet_tail_length, pen=self.pen, timestamp=timestamp)
                items.append(path)
        return items
