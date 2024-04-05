from PyQt5.QtGui import QPen, QBrush, QColor

from .base import VisualizationModule
from ..pyqt_helper import visualize_objects, color_random, polygon2d
from ...road import Lane, Sign, Border, LateralMarking, FlatMarking, Boundary
from ...enums import ReferenceTypes


class VisualizeBorders(VisualizationModule):
    def __init__(self, **kwargs):
        super().__init__('Borders', **kwargs)
        self.show_lane_id = False
        self.color = QColor(250, 250, 250, 120)
        self.width = 0.1

        # Qt elements initiated later on
        self.q_show_lane_id = None
        self.q_color = None
        self.q_width = None

    def extend_config(self):

        self.q_show_lane_id = self._add_checkbox("Show Lane ID on Border", 1, self.show_lane_id)
        self.q_color = self._add_color_select("Color", 3)

        self.q_width = self._add_spinner('Width', 5)
        self.q_width.setMaximum(2.0)
        self.q_width.setSingleStep(0.1)

        self.q_color.setColor(self.color)
        self.q_show_lane_id.setChecked(self.show_lane_id)
        self.q_width.setValue(self.width)

        self.q_show_lane_id.toggled.connect(self._setting_changed_function)
        self.q_color.sigColorChanged.connect(self._setting_changed_function)
        self.q_width.valueChanged.connect(self._setting_changed_function)

    def setting_changed_function(self):
        self.width = self.q_width.value()
        self.color = self.q_color.color()
        self.show_lane_id = self.q_show_lane_id.isChecked()
        self.q_show_lane_id.setEnabled(self.is_visible)
        self.q_color.setEnabled(self.is_visible)
        self.q_width.setEnabled(self.is_visible)

    def visualize_statics(self, snip, visualizer):
        items = []

        pen = QPen(self.color)
        pen.setWidthF(self.width)
        brush = QBrush(self.color)

        i = 0
        for rid, road in snip.reference.roads.items():
            for bid, border in road.borders.items():
                i = i + 1
                text = str(int((i - ((i + 1) % 2)) / 2 - 0.5)) if self.show_lane_id else None
                border_item = visualize_objects(snip.reference, (rid, bid), Border, pen=pen, brush=brush,
                                                text=text)
                items.append(border_item)
        return items


class VisualizeBoundaries(VisualizationModule):
    def __init__(self, name='Boundaries',  **kwargs):
        super().__init__(name=name, **kwargs)
        self.show_boundary_type = True
        self.use_random_color = False
        self.color = QColor(0, 250, 150, 120)
        self.boundary_filter_active = False
        self.boundary_id_filter = -1
        self.lane_filter_active = False
        self.lane_id_filter = -1
        self.road_filter_active = False
        self.road_id_filter = -1
        self.width = 0.05

        # Qt elements initiated later on
        self.q_show_boundary_type = None
        self.q_random_colors = None
        self.q_color = None
        self.q_boundary_filter = None
        self.q_lane_filter = None
        self.q_road_filter = None
        self.q_width = None

    def extend_config(self):
        self.q_show_boundary_type = self._add_checkbox("Show Boundary type", 1, self.show_boundary_type)
        self.q_random_colors = self._add_checkbox("Use Random Colors", 2, self.use_random_color)
        self.q_color = self._add_color_select('Color', 3, self.color)

        self.q_boundary_filter = self._add_spinner('Boundary ID Filter', 4)
        self.q_boundary_filter.setMinimum(-1)
        self.q_boundary_filter.setSingleStep(1)
        self.q_boundary_filter.setDecimals(0)
        self.q_boundary_filter.setValue(self.boundary_id_filter)

        self.q_lane_filter = self._add_spinner('Lane ID Filter', 5)
        self.q_lane_filter.setMinimum(-1)
        self.q_lane_filter.setSingleStep(1)
        self.q_lane_filter.setDecimals(0)
        self.q_lane_filter.setValue(self.lane_id_filter)

        self.q_road_filter = self._add_spinner('Road ID Filter', 6)
        self.q_road_filter.setMinimum(-1)
        self.q_road_filter.setSingleStep(1)
        self.q_road_filter.setDecimals(0)
        self.q_road_filter.setValue(self.road_id_filter)

        self.q_width = self._add_spinner('Width', 7)
        self.q_width.setMaximum(2.0)
        self.q_width.setSingleStep(0.1)

        self.q_show_boundary_type.toggled.connect(self._setting_changed_function)
        self.q_random_colors.toggled.connect(self._setting_changed_function)
        self.q_color.sigColorChanged.connect(self._setting_changed_function)
        self.q_boundary_filter.valueChanged.connect(self._setting_changed_function)
        self.q_lane_filter.valueChanged.connect(self._setting_changed_function)
        self.q_road_filter.valueChanged.connect(self._setting_changed_function)
        self.q_width.valueChanged.connect(self._setting_changed_function)

    def setting_changed_function(self):
        self.color = self.q_color.color()
        self.width = self.q_width.value()
        self.boundary_id_filter = self.q_boundary_filter.value()
        self.boundary_filter_active = not self.boundary_id_filter == -1
        self.lane_id_filter = self.q_lane_filter.value()
        self.lane_filter_active = not self.lane_id_filter == -1
        self.road_id_filter = self.q_road_filter.value()
        self.road_filter_active = not self.road_id_filter == -1
        self.color = self.q_color.color()

        self.show_boundary_type = self.q_show_boundary_type.isChecked()
        self.use_random_color = self.q_random_colors.isChecked()

        self.q_width.setValue(self.width)
        self.q_show_boundary_type.setChecked(self.show_boundary_type)
        self.q_random_colors.setChecked(self.use_random_color)

        self.q_show_boundary_type.setEnabled(self.is_visible)
        self.q_random_colors.setEnabled(self.is_visible)
        self.q_lane_filter.setEnabled(self.is_visible)
        self.q_road_filter.setEnabled(self.is_visible)
        self.q_color.setEnabled(not self.use_random_color and self.is_visible)
        self.q_width.setEnabled(self.is_visible)

    def visualize_statics(self, snippet, visualizer):
        items = []
        for rid, road in snippet.reference.roads.items():
            if self.road_filter_active and not self.road_id_filter == rid:
                continue
            for lid, lane in road.lanes.items():
                for bid, boundary in lane.boundaries.items():
                    if self.boundary_filter_active and not self.boundary_id_filter == bid:
                        continue

                    color = self.color if not self.use_random_color else color_random()
                    if self.lane_filter_active:
                        if not self.lane_id_filter == lid:
                            alpha = 20
                        else:
                            alpha = 220
                        color.setAlpha(int(alpha))

                    pen = QPen(color)
                    pen.setWidthF(self.width)
                    brush = QBrush(color)

                    type_string = ReferenceTypes.BoundaryType(boundary.type).name
                    color_string = ReferenceTypes.BoundaryColor(boundary.color).name
                    condition_string = ReferenceTypes.BoundaryCondition(boundary.condition).name
                    tooltip_text = f'Road: {rid},<br>Lane: {lid},<br>Boundary: {bid},<br>Type: {type_string},' \
                                   f'<br>Color: {color_string},<br>Condition: {condition_string},<br>Height: {boundary.height}'
                    type_text = f'{type_string}' if self.show_boundary_type else ''

                    polyline = visualize_objects(input_recording=snippet.reference, index=(rid, lid, bid), cls=Boundary,
                                                 text=type_text, tooltip=tooltip_text, pen=pen, brush=brush)

                    items.append(polyline)
        return items


class VisualizeLanes(VisualizationModule):
    def __init__(self, name='Lanes', **kwargs):
        super().__init__(name=name, **kwargs)
        self.show_lane_id = True
        self.use_random_color = False
        self.color = QColor(0, 150, 250, 120)
        self.lane_filter_active = False
        self.lane_id_filter = -1
        self.road_filter_active = False
        self.road_id_filter = -1

        # Qt elements initiated later on
        self.q_show_line_id = None
        self.q_random_colors = None
        self.q_color = None
        self.q_lane_filter = None
        self.q_road_filter = None

    def extend_config(self):
        self.q_show_line_id = self._add_checkbox("Show Lane ID on Lane", 1, self.show_lane_id)
        self.q_random_colors = self._add_checkbox("Use Random Colors", 2, self.use_random_color)
        self.q_color = self._add_color_select('Color', 3, self.color)

        self.q_lane_filter = self._add_spinner('Lane ID Filter', 4)
        self.q_lane_filter.setMinimum(-1)
        self.q_lane_filter.setSingleStep(1)
        self.q_lane_filter.setDecimals(0)
        self.q_lane_filter.setValue(self.lane_id_filter)

        self.q_road_filter = self._add_spinner('Road ID Filter', 5)
        self.q_road_filter.setMinimum(-1)
        self.q_road_filter.setSingleStep(1)
        self.q_road_filter.setDecimals(0)
        self.q_road_filter.setValue(self.road_id_filter)

        self.q_show_line_id.toggled.connect(self._setting_changed_function)
        self.q_random_colors.toggled.connect(self._setting_changed_function)
        self.q_color.sigColorChanged.connect(self._setting_changed_function)
        self.q_lane_filter.valueChanged.connect(self._setting_changed_function)
        self.q_road_filter.valueChanged.connect(self._setting_changed_function)

    def setting_changed_function(self):
        self.lane_id_filter = self.q_lane_filter.value()
        self.lane_filter_active = not self.lane_id_filter == -1
        self.road_id_filter = self.q_road_filter.value()
        self.road_filter_active = not self.road_id_filter == -1
        self.color = self.q_color.color()
        self.show_lane_id = self.q_show_line_id.isChecked()
        self.use_random_color = self.q_random_colors.isChecked()

        self.q_show_line_id.setChecked(self.show_lane_id)
        self.q_random_colors.setChecked(self.use_random_color)

        self.q_show_line_id.setEnabled(self.is_visible)
        self.q_random_colors.setEnabled(self.is_visible)
        self.q_lane_filter.setEnabled(self.is_visible)
        self.q_road_filter.setEnabled(self.is_visible)
        self.q_color.setEnabled(not self.use_random_color and self.is_visible)

    def visualize_statics(self, snip, visualizer):
        items = []
        for road_id, road in snip.reference.roads.items():
            if self.road_filter_active:
                if not self.road_id_filter == road_id:
                    continue
            for lane_id, lane in road.lanes.items():
                color = self.color if not self.use_random_color else color_random()
                pen = QPen(color)
                pen.setWidth(0)

                brush = QBrush(color)
                brush_color = brush.color()
                if self.lane_filter_active:
                    if not self.lane_id_filter == lane_id:
                        alpha = 20
                    else:
                        alpha = 220
                    brush_color.setAlpha(int(alpha))
                    brush.setColor(brush_color)

                poly = visualize_objects(input_recording=snip.reference, index=(road_id, lane_id), cls=Lane, pen=pen,
                                         brush=brush, text=f'[r{road_id},l{lane_id}]{lane.type.name}' if self.show_lane_id else None)
                items.append(poly)
        return items


class VisualizeLateralMarkings(VisualizationModule):
    def __init__(self, **kwargs):
        super().__init__('Lateral Markings', **kwargs)
        self.show_lateral_marking_type = True
        self.use_random_color = False
        self.color = QColor(250, 150, 0, 120)
        self.road_filter_active = False
        self.road_id_filter = -1
        self.width = 0.05

        # Qt elements initiated later on
        self.q_show_lateral_marking_type = None
        self.q_random_colors = None
        self.q_color = None
        self.q_lane_filter = None
        self.q_road_filter = None
        self.q_width = None

    def extend_config(self):
        self.q_show_lateral_marking_type = self._add_checkbox("Show type", 1, self.show_lateral_marking_type)
        self.q_random_colors = self._add_checkbox("Use Random Colors", 2, self.use_random_color)
        self.q_color = self._add_color_select('Color', 3, self.color)

        self.q_road_filter = self._add_spinner('Road ID Filter', 5)
        self.q_road_filter.setMinimum(-1)
        self.q_road_filter.setSingleStep(1)
        self.q_road_filter.setDecimals(0)
        self.q_road_filter.setValue(self.road_id_filter)

        self.q_width = self._add_spinner('Width', 6)
        self.q_width.setMaximum(2.0)
        self.q_width.setSingleStep(0.1)
        self.q_width.setValue(self.width)

        self.q_show_lateral_marking_type.toggled.connect(self._setting_changed_function)
        self.q_random_colors.toggled.connect(self._setting_changed_function)
        self.q_color.sigColorChanged.connect(self._setting_changed_function)
        self.q_road_filter.valueChanged.connect(self._setting_changed_function)
        self.q_width.valueChanged.connect(self._setting_changed_function)

    def setting_changed_function(self):
        self.color = self.q_color.color()
        self.width = self.q_width.value()
        self.road_id_filter = self.q_road_filter.value()
        self.road_filter_active = not self.road_id_filter == -1
        self.color = self.q_color.color()

        self.show_lateral_marking_type = self.q_show_lateral_marking_type.isChecked()
        self.use_random_color = self.q_random_colors.isChecked()

        self.q_width.setValue(self.width)
        self.q_show_lateral_marking_type.setChecked(self.show_lateral_marking_type)
        self.q_random_colors.setChecked(self.use_random_color)

        self.q_show_lateral_marking_type.setEnabled(self.is_visible)
        self.q_random_colors.setEnabled(self.is_visible)
        self.q_road_filter.setEnabled(self.is_visible)
        self.q_color.setEnabled(not self.use_random_color and self.is_visible)
        self.q_width.setEnabled(self.is_visible)

    def visualize_statics(self, snip, visualizer):
        items = []
        for rid, road in snip.reference.roads.items():
            if self.road_filter_active:
                if not self.road_id_filter == rid:
                    continue
            for lid, lateral_marking in road.lateral_markings.items():
                color = self.color if not self.use_random_color else color_random()
                pen = QPen(color)
                pen.setWidthF(self.width)
                brush = QBrush(color)

                type_string = ReferenceTypes.LateralMarkingType(lateral_marking.type).name
                color_string = ReferenceTypes.LateralMarkingColor(lateral_marking.color).name
                condition_string = ReferenceTypes.LateralMarkingCondition(lateral_marking.condition).name
                tooltip_text = f'Road: {rid},<br>LateralMarking: {lid},<br>Type: {type_string},' \
                               f'<br>Color: {color_string},<br>Condition: {condition_string},<br>Depth: {lateral_marking.long_size}'
                type_text = f'{type_string}' if self.show_lateral_marking_type else ''

                polyline = visualize_objects(snip.reference, (rid, lid), LateralMarking, pen=pen, brush=brush,
                                             text=type_text, tooltip=tooltip_text)
                items.append(polyline)
        return items


class VisualizeFlatMarkings(VisualizationModule):
    def __init__(self, **kwargs):
        super().__init__('Flat Markings', **kwargs)
        self.show_flat_marking_type = True
        self.use_random_color = False
        self.color = QColor(250, 150, 0, 120)
        self.road_filter_active = False
        self.road_id_filter = -1
        self.width = 0.05

        # Qt elements initiated later on
        self.q_show_flat_marking_type = None
        self.q_random_colors = None
        self.q_color = None
        self.q_lane_filter = None
        self.q_road_filter = None
        self.q_width = None

    def extend_config(self):
        self.q_show_flat_marking_type = self._add_checkbox("Show type", 1, self.show_flat_marking_type)
        self.q_random_colors = self._add_checkbox("Use Random Colors", 2, self.use_random_color)
        self.q_color = self._add_color_select('Color', 3, self.color)

        self.q_road_filter = self._add_spinner('Road ID Filter', 5)
        self.q_road_filter.setMinimum(-1)
        self.q_road_filter.setSingleStep(1)
        self.q_road_filter.setDecimals(0)
        self.q_road_filter.setValue(self.road_id_filter)

        self.q_width = self._add_spinner('Width', 6)
        self.q_width.setMaximum(2.0)
        self.q_width.setSingleStep(0.1)
        self.q_width.setValue(self.width)

        self.q_show_flat_marking_type.toggled.connect(self._setting_changed_function)
        self.q_random_colors.toggled.connect(self._setting_changed_function)
        self.q_color.sigColorChanged.connect(self._setting_changed_function)
        self.q_road_filter.valueChanged.connect(self._setting_changed_function)
        self.q_width.valueChanged.connect(self._setting_changed_function)

    def setting_changed_function(self):
        self.color = self.q_color.color()
        self.width = self.q_width.value()
        self.road_id_filter = self.q_road_filter.value()
        self.road_filter_active = not self.road_id_filter == -1
        self.color = self.q_color.color()

        self.show_flat_marking_type = self.q_show_flat_marking_type.isChecked()
        self.use_random_color = self.q_random_colors.isChecked()

        self.q_width.setValue(self.width)
        self.q_show_flat_marking_type.setChecked(self.show_flat_marking_type)
        self.q_random_colors.setChecked(self.use_random_color)

        self.q_show_flat_marking_type.setEnabled(self.is_visible)
        self.q_random_colors.setEnabled(self.is_visible)
        self.q_road_filter.setEnabled(self.is_visible)
        self.q_color.setEnabled(not self.use_random_color and self.is_visible)
        self.q_width.setEnabled(self.is_visible)

    def visualize_statics(self, snip, visualizer):
        items = []
        for rid, road in snip.reference.roads.items():
            if self.road_filter_active:
                if not self.road_id_filter == rid:
                    continue
            for lid, lane in road.lanes.items():
                for fid, flat_marking in lane.flat_markings.items():
                    color = self.color if not self.use_random_color else color_random()
                    pen = QPen(color)
                    pen.setWidthF(self.width)
                    brush = QBrush(color)

                    type_string = ReferenceTypes.FlatMarkingType(flat_marking.type).name
                    color_string = ReferenceTypes.FlatMarkingColor(flat_marking.color).name
                    condition_string = ReferenceTypes.FlatMarkingCondition(flat_marking.condition).name
                    tooltip_text = f'Road: {rid},<br>FlatMarking: {fid},<br>Type: {type_string},' \
                                   f'<br>Color: {color_string},<br>Condition: {condition_string}'
                    type_text = f'{type_string}' if self.show_flat_marking_type else ''

                    polyline = visualize_objects(snip.reference, (rid, lid, fid), FlatMarking, pen=pen, brush=brush,
                                                 text=type_text, tooltip=tooltip_text)

                    items.append(polyline)
        return items


class VisualizeSigns(VisualizationModule):
    def __init__(self, **kwargs):
        super().__init__('Signs', **kwargs)
        self.color = QColor(250, 150, 0, 120)
        self.road_filter_active = False
        self.road_id_filter = -1
        self.size = 1.0

        # Qt elements initiated later on
        self.q_color = None
        self.q_road_filter = None
        self.q_size = None

    def extend_config(self):
        self.q_color = self._add_color_select('Color', 3, self.color)

        self.q_road_filter = self._add_spinner('Road ID Filter', 5)
        self.q_road_filter.setMinimum(-1)
        self.q_road_filter.setSingleStep(1)
        self.q_road_filter.setDecimals(0)
        self.q_road_filter.setValue(self.road_id_filter)

        self.q_size = self._add_spinner('Size', 6)
        self.q_size.setMaximum(2.0)
        self.q_size.setSingleStep(0.1)
        self.q_size.setValue(self.size)

        self.q_color.sigColorChanged.connect(self._setting_changed_function)
        self.q_road_filter.valueChanged.connect(self._setting_changed_function)
        self.q_size.valueChanged.connect(self._setting_changed_function)

    def setting_changed_function(self):
        self.color = self.q_color.color()
        self.size = self.q_size.value()
        self.road_id_filter = self.q_road_filter.value()
        self.road_filter_active = not self.road_id_filter == -1

        self.q_size.setValue(self.size)

        self.q_road_filter.setEnabled(self.is_visible)
        self.q_color.setEnabled(self.is_visible)
        self.q_size.setEnabled(self.is_visible)

    def visualize_statics(self, snip, visualizer):
        items = []
        for rid, road in snip.reference.roads.items():

            if self.road_filter_active and not self.road_id_filter == rid:
                continue
            for sid, sign in road.signs.items():
                pen = QPen(self.color)
                pen.setWidthF(0)
                brush = QBrush(self.color)

                type_string = ReferenceTypes.SignType(sign.type).name
                tooltip_text = f'Road: {rid},<br>Sign: {sid},<br>Type: {type_string},<br>Heading: {sign.heading:1.4f}'
                type_text = f'{type_string}'

                polyline = visualize_objects(snip.reference, (rid, sid), Sign, pen=pen, brush=brush, text=type_text,
                                             tooltip=tooltip_text)
                items.append(polyline)
        return items


class VisualizeStructural(VisualizationModule):
    def __init__(self, **kwargs):
        super().__init__('Structural', **kwargs)

    def visualize_statics(self, snip, visualizer):
        col = QColor(0, 250, 150, 120)
        pen = QPen(col)
        pen.setWidthF(0)
        brush = QBrush(col)
        return [polygon2d(tuples=list(zip(obj.polyline.pos_x, obj.polyline.pos_y)), pen=pen, brush=brush,
                          text=obj.type.name)
                for r in snip.reference.roads.values() for obj in r.structural_objects.values()]


class VisualizeRoadObjects(VisualizationModule):
    def __init__(self, **kwargs):
        super().__init__('RoadObjects', **kwargs)

    def visualize_statics(self, snip, visualizer):
        col = QColor(90, 90, 90, 120)
        pen = QPen(col)
        pen.setWidthF(0)
        brush = QBrush(col)
        return [polygon2d(tuples=list(zip(obj.polyline.pos_x, obj.polyline.pos_y)), pen=pen, brush=brush,
                          text=obj.type.name)
                for r in snip.reference.roads.values() for obj in r.road_objects.values()]
