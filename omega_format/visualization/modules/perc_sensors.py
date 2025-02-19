import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets

from .base import VisualizationModule, SnippetContainer


class VisualizePercSensors(VisualizationModule):

    def __init__(self, **kwargs):
        super().__init__("Perception: Sensors FOV", **kwargs)
        self.requires = [SnippetContainer.REQ_PERCEPTION]

    def visualize_dynamics(self, snip, timestamp, visualizer):
        if snip.identifier != 'only_perception' and not snip.reference.ego_vehicle.in_timespan(timestamp, timestamp):
            return []

        items = []
        ego_offset = snip.perception.ego_offset

        if snip.identifier != 'only_perception':
            ego_obj = snip.reference.ego_vehicle
            ego_index = timestamp - ego_obj.birth

            ego_x = ego_obj.tr.pos_x[ego_index]
            ego_y = ego_obj.tr.pos_y[ego_index]
            ego_h = ego_obj.tr.heading[ego_index]

        for id_, sensor in snip.perception.sensors.items():  # type: int, Sensor
            offset_x = sensor.sensor_pos_lateral
            offset_y = sensor.sensor_pos_longitudinal + ego_offset

            heading = sensor.sensor_heading
            dist_max = sensor.max_range
            diameter = dist_max * 2
            fov_horizontal = sensor.fov_horizontal

            start_angle = -fov_horizontal/2
            span_angle = fov_horizontal

            artist = QtWidgets.QGraphicsEllipseItem(-diameter / 2, -diameter / 2, diameter, diameter)
            artist.setStartAngle(start_angle * 16)
            artist.setSpanAngle(span_angle * 16)

            color = '#ffffff'
            pen = pg.mkPen(color, width=1)
            brush = pg.mkBrush(color + '44')

            artist.setPen(pen)
            artist.setBrush(brush)

            center_point = artist.boundingRect().center()
            artist.translate(-center_point.x(), -center_point.y())
            if snip.identifier != 'only_perception':
                artist.setRotation(heading + ego_h)
            else:
                artist.setRotation(heading + 90)
            artist.translate(center_point.x(), center_point.y())

            if snip.identifier != 'only_perception':
                new_x = np.multiply(offset_y, np.cos(np.deg2rad(ego_h))) - np.multiply(offset_x, np.sin(np.deg2rad(ego_h))) + ego_x
                new_y = np.multiply(offset_y, np.sin(np.deg2rad(ego_h))) + np.multiply(offset_x, np.cos(np.deg2rad(ego_h))) + ego_y
                artist.translate(new_x, new_y)
            else:
                artist.translate(offset_x, offset_y)

            items.append(artist)


        return items
