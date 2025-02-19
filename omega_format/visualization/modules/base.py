from collections import deque
from enum import Enum
from typing import Optional, List, Callable

import numpy as np
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QCheckBox, QDoubleSpinBox, QSpinBox
from PyQt5.QtCore import QCoreApplication
from pyqtgraph import ColorButton

from ...reference_recording import ReferenceRecording
from ...perception_recording import PerceptionRecording



class SnippetContainer():

    @classmethod
    def REQ_REFERENCE(cls, self):
        return hasattr(self, 'reference') and self.reference is not None

    @classmethod
    def REQ_PERCEPTION(cls, self):
        return hasattr(self, 'perception') and self.perception is not None

    def check_requirements(self, module):
        return np.all([r(self) for r in module.requires])

    def __init__(self, reference: Optional[ReferenceRecording]=None, perception: Optional[PerceptionRecording]=None):
        self.reference = reference
        self.perception = perception
        if self.reference is not None:
            if self.perception is not None:
                if self.reference.ego_vehicle is None:
                    self.reference.ego_id = self.perception.ego_id
                    self.reference.ego_vehicle = self.reference.road_users[self.reference.ego_id]
                    self.reference.road_users.pop(self.reference.ego_id, None)
                self.convert_perception_coordinates_to_reference_coordinates()
                self.adjust_perception_object_birth_stamps()

            self.timestamps = self.reference.timestamps
            self.identifier = '' if self.reference.ego_id is None else f'ego_id: {self.reference.ego_id}'
        elif self.perception is not None:
            self.timestamps = perception.timestamps
            self.identifier = 'only_perception'
            self.convert_perception_coordinates_to_plot_coordinates()
        else:
            raise ValueError('Either `reference` or `perception` has to be set')

    @classmethod
    def create_list(cls, references=None, perceptions=None):
        if (isinstance(references, list)) or (isinstance(perceptions, list)):
            if references is None:
                return [cls(perception=p) for p in perceptions]
            elif perceptions is None:
                return [cls(reference=r) for r in references]
            elif len(references) == len(perceptions):
                return [cls(reference=r, perception=p) for r, p in zip(references, perceptions)]
            else:
                raise ValueError('`reference` and `perception` must be of the same length!')
        else:
            return [cls(reference=references, perception=perceptions)]

    def convert_perception_coordinates_to_plot_coordinates(self):
        for obj in self.perception.objects.values():  # type: Object
            x = -obj.dist_lateral.val
            y = obj.dist_longitudinal.val
            heading = 180
            obj.heading.val += heading/2
            obj.dist_lateral.val = - np.multiply(x, np.cos(np.deg2rad(heading))) + np.multiply(y, np.sin(np.deg2rad(heading)))
            obj.dist_longitudinal.val = - np.multiply(x, np.sin(np.deg2rad(heading))) - np.multiply(y, np.cos(np.deg2rad(heading)))

    def convert_perception_coordinates_to_reference_coordinates(self):
         for obj in self.perception.objects.values():  # type: Object
            death = obj.birth_stamp+len(obj.heading.val)
            obj.dist_longitudinal.val += self.perception.ego_offset # adjust ego offset

            ego_h = self.reference.ego_vehicle.tr.heading[obj.birth_stamp:death]
            ego_x = self.reference.ego_vehicle.tr.pos_x[obj.birth_stamp:death]
            ego_y = self.reference.ego_vehicle.tr.pos_y[obj.birth_stamp:death]
            x = -obj.dist_lateral.val
            y = obj.dist_longitudinal.val
            heading = ego_h + 270
            obj.dist_lateral.val = np.multiply(x, np.cos(np.deg2rad(heading))) - np.multiply(y, np.sin(np.deg2rad(heading)))+ego_x
            obj.dist_longitudinal.val = np.multiply(x, np.sin(np.deg2rad(heading))) + np.multiply(y, np.cos(np.deg2rad(heading)))+ego_y
            obj.heading.val += ego_h

    def adjust_perception_object_birth_stamps(self):
        ego_time_offset = self.reference.ego_vehicle.birth
        for obj in self.perception.objects.values():  # type: Object
            obj.birth_stamp += ego_time_offset



class VisualizationModuleType(Enum):
    CONFIG_VISUALIZER = 1,
    STATIC_ENVIRONMENT = 2,
    DYNAMIC_ENVIRONMENT = 3,
    METADATA_RECORDING = 4,
    HIDE = 5


class VisualizationModuleManager(object):

    def __init__(self, name=None, is_visible=True, typ=VisualizationModuleType.CONFIG_VISUALIZER, requires: Optional[List[Callable]]=None):
        if requires is None:
            requires = [SnippetContainer.REQ_REFERENCE]
        self.label = name if name else self.__class__.__name__
        self.is_visible = is_visible
        self.requires = requires
        self.type = typ
        self.visualizer = None
        self._dynamic_visualized_items = deque()
        self._static_visualized_items = deque()
        self._plots = deque()

        self.q_label = None
        self.q_container = None
        self.q_grid_layout = None
        self.q_visible = None

    def config(self, visualizer):
        self.q_label = QLabel()
        self.q_label.setText(QCoreApplication.translate("MainWindow", self.label))
        self.q_container = QWidget()
        self.q_grid_layout = QGridLayout(self.q_container)
        self.q_grid_layout.setColumnStretch(0, 0)
        self.q_grid_layout.setColumnStretch(1, 1)
        self.q_visible = self._add_checkbox("Visible", 0, self.is_visible)

        self.extend_config()

        self.visualizer = visualizer
        self.q_visible.toggled.connect(self._setting_changed_function)
        return [self.q_label, self.q_container]

    def extend_config(self):
        raise NotImplementedError

    def _setting_changed_function(self):
        self.is_visible = self.q_visible.isChecked()

        self.setting_changed_function()

        self.update_statics(self.visualizer.snippet)
        self.update_dynamics(self.visualizer.snippet, self.visualizer.current_frame)

    def setting_changed_function(self):
        raise NotImplementedError

    def visualize_dynamics(self, snip: SnippetContainer, timestamp, visualizer):
        raise NotImplementedError

    def visualize_statics(self, snip: SnippetContainer, visualizer):
        raise NotImplementedError

    def plot_timeseries(self, snip: SnippetContainer, visualizer):
        raise NotImplementedError

    def update_dynamics(self, snip: SnippetContainer, timestamp):
        self.remove_visualized_items(only_dynamic=True)
        items = self.visualize_dynamics(snip, timestamp, self.visualizer) if self.is_visible and snip.check_requirements(self) else []
        for item in items:
            self._dynamic_visualized_items.append(item)
            self.visualizer.canvas.addItem(item)

    def update_statics(self, snip: SnippetContainer):
        self.remove_visualized_items(only_dynamic=False)
        items = self.visualize_statics(snip, self.visualizer) if self.is_visible and snip.check_requirements(self) else []
        for item in items:
            self._static_visualized_items.append(item)
            self.visualizer.canvas.addItem(item)

        ps = self.plot_timeseries(snip, self.visualizer) if self.is_visible and snip.check_requirements(self) else []
        for p in ps:
            self._plots.append(p)
            self.visualizer.timeseriesplot.addItem(p)

    def remove_visualized_items(self, only_dynamic=True):
        """
        Removes all dynamic items from visualization for the last frame
        """

        while self._dynamic_visualized_items:
            item = self._dynamic_visualized_items.pop()
            self.visualizer.canvas.removeItem(item)

        if not only_dynamic:
            while self._static_visualized_items:
                item = self._static_visualized_items.pop()
                self.visualizer.canvas.removeItem(item)
            while self._plots:
                item = self._plots.pop()
                self.visualizer.timeseriesplot.removeItem(item)

    # Helper functions for quick config
    def _add_checkbox(self, text, row, is_checked=True):
        checkbox = QCheckBox(self.q_container)
        checkbox.setChecked(is_checked)
        checkbox.setText(QCoreApplication.translate("MainWindow", text))
        self.q_grid_layout.addWidget(checkbox, row, 0, 1, 2)
        return checkbox

    def _add_color_select(self, text, row, color=None):
        lbl = QLabel()
        lbl.setText(QCoreApplication.translate("MainWindow", text))
        self.q_grid_layout.addWidget(lbl, row, 0, 1, 1)
        color_select = ColorButton(self.q_container)
        font = QFont()
        font.setFamily("Material Icons")
        color_select.setFont(font)
        if color:
            color_select.setColor(color)
        self.q_grid_layout.addWidget(color_select, row, 1, 1, 1)

        return color_select

    def _add_spinner(self, text, row, double=True):
        lbl = QLabel(self.q_container)
        lbl.setText(QCoreApplication.translate("MainWindow", text))
        self.q_grid_layout.addWidget(lbl, row, 0, 1, 1)
        if double:
            spinner = QDoubleSpinBox(self.q_container)
        else:
            spinner = QSpinBox(self.q_container)
        self.q_grid_layout.addWidget(spinner, row, 1, 1, 1)
        return spinner


class VisualizationModule(VisualizationModuleManager):
    '''
    With this Module you can add your own Elements to the Visualizations of the Visualizer by just subclassing this module.
    Only use the functions defined below.
    '''
    def __init__(self, name=None, is_visible=True, typ=VisualizationModuleType.CONFIG_VISUALIZER, requires: List[Callable]=[SnippetContainer.REQ_REFERENCE]):
        super().__init__(name=name, is_visible=is_visible, typ=typ)

    def extend_config(self):
        """
        Use this function to add additional settings to the module. By default, every module has a checkbox to toggle the visibility of the module. You can either use one of the functions `_add_checkbox`, `_add_spinner` or `_add_color_select` or directly add a widget to the settings grid layout of the module accessible by the property `self.q_grid_layout`. It is best practice to connect all callbacks to `self._setting_changed_function`. Then you can handle your logic in `setting_changed_function`.
        """
        pass

    def setting_changed_function(self):
        """
        In this function, the logic that handles changes of settings should be placed. The visibility toggle is handled automatically.
        """
        pass

    def visualize_dynamics(self, snip: SnippetContainer, timestamp: int, visualizer):
        """
        use this function to add elements that depend on the timestamp. Each timestep, the old elements are deleted.
        As return, a list of the QGraphicsItems to show are expected. The plotting itself is automatically
        handled by the parent Class `VisualizationModuleManager`.
        """
        return []

    def visualize_statics(self, snip: SnippetContainer, visualizer):
        """
        use this function to add elements that are constant over time. This function is only called when the visiblity status
        of the module changes or if the snippet is switched. As return, a list of the QGraphicsItems to show are expected.
        The plotting itself is automatically handled by the parent Class `VisualizationModuleManager`.
        """
        return []

    def plot_timeseries(self, snip: SnippetContainer, visualizer):
        """
        use this function to add timeseries plots to the plotview. The function is called in conjunction with `visualize_statics`.
        A list of `pyqtgraph.DataPlotIem` is expected as return.
        """
        return []