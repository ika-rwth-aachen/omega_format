# ruff: noqa: F405
import sys
from pathlib import Path
from typing import List

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import QPoint, QSize, QSettings, QTimer, QSignalMapper, Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow

from .modules import * # noqa: F403


class Visualizer(QMainWindow):
    def __init__(self, snippets: List[SnippetContainer], title="", default_pause=False, visualizers=None, use_default_visualizers=True):

        self._app = pg.mkQApp()
        self._app.setOrganizationName('Institut für Kraftfahrzeuge Aachen')
        self._app.setOrganizationDomain('www.ika.rwth-aachen.de')
        self._app.setApplicationName('OMEGAFormat Visualizer')
        self._app.setStyle("Fusion")
        self._app.setWindowIcon(QIcon(str(Path(__file__).parent.resolve()/'ui/icon.svg')))

        super().__init__()

        self.fps = 0.0
        self._current_frame = 0

        self._title = title
        self._ui_path_and_file = Path(__file__).parent.resolve() / 'ui/main.ui'

        self._paused = False
        self.visualizers = visualizers

        self.snippets = snippets
        self.timeseriesindicator = None
        self.visualizers = visualizers if visualizers is not None else []
        if use_default_visualizers:
            ref = [VisualizeTP(text_funcs=[objects.print_speed]),
                VisualizeTPPath(),
                VisualizeLanes(),
                VisualizeBorders(is_visible=False),
                VisualizeBoundaries(is_visible=False),
                VisualizeLateralMarkings(),
                VisualizeFlatMarkings(),
                VisualizeSigns(),
                VisualizeStructural(),
                VisualizeRoadObjects(),
                VisualizeWeather()
            ] if self.snippets[0].reference is not None else []


            perc = [VisualizePerc(text_funcs=[perc_objects.print_heading,
                                          perc_objects.print_speed]),
                    VisualizePercPath(),
                    VisualizePercSensors()
                    ] if self.snippets[0].perception is not None else []
            self.visualizers = ref + perc + self.visualizers

        self._timer = QTimer()
        self._timer.timeout.connect(self.visualize_next_frame)
        self._default_pause = default_pause

    @property
    def input_recording(self):
        return self.snippet.reference

    def start_gui_and_visualization(self):
        """
        starts the gui and animation
        """
        self.selected_snippet = 0
        self.snippet = self.snippets[self.selected_snippet]
        # Load gui after anything is set
        self._connect_gui_and_functions()
        # Render first snippet
        self.select_snippet(0)
        # Fixing the viewport to items from first scene
        self.canvas.autoRange()


        self.show()
        sys.exit(self._app.exec_())

    def visualize_next_frame(self, pause=False):
        """
        Visualizes the next frame including wrap around

        :param pause: bool whether to pause after visualizing the frame, defaults to False
        :type pause: bool, optional
        """
        if pause:
            self.pause()
        self.current_frame += 1
        self.visualize()

    def visualize_previous_frame(self, pause=False):
        """
        Visualizes the next frame including wrap around

        :param pause: bool whether to pause after visualizing the frame, defaults to False
        :type pause: bool, optional
        """

        if pause:
            self.pause()
        self.current_frame -= 1
        self.visualize()

    def elapsed_time(self, index):
        # if no time information
        if len(self.snippet.timestamps) == 0:
            return 0
        return (self.snippet.timestamps[index] - self.snippet.timestamps[0])


    def visualize(self):
        """
        Main Visualization function
        """
        self.slider.setValue(self.current_frame)

        # update labels
        self.lbl_current_frame.setText(str(self._current_frame))
        self.lbl_current_time.setText('{: <0.2f} sec'.format(self.elapsed_time(self._current_frame)))



        for vis in self.visualizers:
            vis.update_dynamics(self.snippet, self._current_frame)

        if self.timeseriesindicator is not None:
            self.timeseriesplot.removeItem(self.timeseriesindicator)
        self.timeseriesindicator = self.timeseriesplot.addLine(x=self._current_frame)

    def select_snippet(self, value: int):
        self.pause()
        self.selected_snippet = int(value)
        self.snippet = self.snippets[self.selected_snippet]

        window_title = f'omega_format - {self._title}'
        if self.snippets[0].reference is not None:
            window_title += f' - snippet {self.selected_snippet}'
        self.setWindowTitle(window_title)

        self._current_frame = 0
        self.reload_gui()

        self.visualize()
        if not self._default_pause:
            self.play()

    def set_fps(self, value: float):
        """
        Sets the fps

        :param value:
        """
        if value != value or value == 0:
            self.fps = 25
        else:
            self.fps = value
        self._timer.setInterval(int(1000.0 / self.fps))

    def _compute_fps(self):
        self._last_frame = len(self.snippet.timestamps) - 1
        self.set_fps(1 / np.median(np.diff(self.snippet.timestamps)))

    def _connect_gui_and_functions(self):
        """
        Connects the gui functionality like buttons and checkboxes to their methods
        """
        super().__init__()
        uic.loadUi(self._ui_path_and_file, self)
        self._read_window_state()

        self.canvas.setAspectLocked(True)
        self.canvas.setFocus()
        self.canvas.setAntialiasing(True)
        self.canvas.setBackground(QColor(53, 53, 53))


        self.timeseriesplot.setAntialiasing(True)
        self.timeseriesplot.setMouseEnabled(False, False)
        self.timeseriesplot.addLegend()
        self.timeseriesplot.enableAutoRange(True)


        # Add snippet selection
        menu_mapping = QSignalMapper(self)
        for index, snippet in enumerate(self.snippets):
            text = f'{index}: {snippet.identifier}, frames: {len(snippet.timestamps)}'
            action = self.menu_select_snippet.addAction(text)
            menu_mapping.setMapping(action, index)
            action.triggered.connect(menu_mapping.map)
        menu_mapping.mapped.connect(self.select_snippet)

        for visualizer in self.visualizers:
            for widget in visualizer.config(self):
                if visualizer.type == VisualizationModuleType.CONFIG_VISUALIZER:
                    widget.setParent(self.container_config_content)
                    self.vertical_layout_config.addWidget(widget)
                elif visualizer.type == VisualizationModuleType.STATIC_ENVIRONMENT:
                    widget.setParent(self.container_static_environment_content)
                    self.vertical_layout_static_environment.addWidget(widget)
                elif visualizer.type == VisualizationModuleType.DYNAMIC_ENVIRONMENT:
                    widget.setParent(self.container_dynamic_environment_content)
                    self.vertical_layout_dynamic_environment.addWidget(widget)
                elif visualizer.type == VisualizationModuleType.METADATA_RECORDING:
                    widget.setParent(self.container_recording_meta_data_content)
                    self.vertical_layout_recording_meta_data.addWidget(widget)

            if visualizer.type == VisualizationModuleType.HIDE:
                continue

            line = QtWidgets.QFrame(self.container_config_content)
            line.setFrameShadow(QtWidgets.QFrame.Plain)
            line.setFrameShape(QtWidgets.QFrame.HLine)
            if visualizer.type == VisualizationModuleType.CONFIG_VISUALIZER:
                self.vertical_layout_config.addWidget(line)
            elif visualizer.type == VisualizationModuleType.STATIC_ENVIRONMENT:
                self.vertical_layout_static_environment.addWidget(line)
            elif visualizer.type == VisualizationModuleType.DYNAMIC_ENVIRONMENT:
                self.vertical_layout_dynamic_environment.addWidget(line)
            elif visualizer.type == VisualizationModuleType.METADATA_RECORDING:
                self.vertical_layout_recording_meta_data.addWidget(line)
            visualizer.setting_changed_function()
        # Set minimum size to prevent horizontal scrollbar from appearing
        minimum_size: QSize = self.container_config_content.sizeHint()
        minimum_size.setWidth(minimum_size.width() + 30)
        minimum_size.setHeight(0)
        self.container_config.setMinimumSize(minimum_size)
        minimum_size: QSize = self.container_static_environment_content.sizeHint()
        minimum_size.setWidth(minimum_size.width() + 30)
        minimum_size.setHeight(0)
        self.container_config.setMinimumSize(minimum_size)

        # Connect anything
        self.action_terminate_application.triggered.connect(lambda: sys.exit())
        self.pb_play_pause.clicked.connect(self.play_pause)
        self.pb_next.clicked.connect(lambda: self.visualize_next_frame(True))
        self.pb_back.clicked.connect(lambda: self.visualize_previous_frame(True))

    def _store_window_state(self):
        settings = QSettings()

        settings.beginGroup("MainWindow")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        settings.endGroup()

    def _read_window_state(self):
        settings = QSettings()
        settings.beginGroup("MainWindow")
        self.resize(settings.value("size", QSize(960, 680)))
        self.move(settings.value("pos", QPoint(200, 200)))
        settings.endGroup()

    def update_sliders(self):
        self.slider.setMinimum(0)
        self.slider.setMaximum(self._last_frame)
        self.slider.sliderMoved.connect(self._slider_step)

    def update_labels(self):
        self.lbl_total_frames.setText(str(self._last_frame))
        self.lbl_total_time.setText('{: <0.2f} sec'.format(self.elapsed_time(-1)))

    def reload_gui(self):
        self._compute_fps()
        self.update_sliders()
        self.update_labels()
        for vis in self.visualizers:
            vis.update_statics(self.snippet)
        self.timeseriesplot.setXRange(0, len(self.snippet.timestamps), padding=0)
        self.visualize()

    def closeEvent(self, event):
        """
        Exits child windows when the main window gets closed

        :param event: close event
        :type event: QtGui.QCloseEvent
        """

        self._store_window_state()
        self._timer.stop()
        self.canvas.close()
        self.timeseriesplot.close()
        self.close()

    def keyPressEvent(self, event):
        """
        Method used for keyboard functionality, inherited from QtWidgets.QMainWindow

        :param event: pressed key
        :type event: QtWidgets.QKeyEvent
        """

        if event.key() == Qt.Key_Space or event.key() == Qt.Key_Return:
            self.play_pause()
        elif event.key() == Qt.Key_Left:
            self.visualize_previous_frame(True)
        elif event.key() == Qt.Key_Right:
            self.visualize_next_frame(True)

    def _update_frame(self):
        """
        Is called when something in the gui is changed and the frame should be updated
        """

        if self._paused:
            self.visualize()

    def _slider_step(self, value: int):
        """
        Is called when the slider was moved, animates the selected frame

        :param value: frame number
        :type value: int
        """
        self.pause()
        self.current_frame = value
        self.visualize()

    def play_pause(self):
        """
        Plays or pauses the animation
        """

        self._paused = not self._paused
        if self._paused:
            self.pause()
        else:
            self.play()

    def pause(self):
        """
        Pauses the animation
        """

        self._timer.stop()
        self._paused = True
        self.pb_play_pause.setText('▶')

    def play(self):
        """
        Plays the animation
        """

        self._timer.start()
        self._paused = False
        self.pb_play_pause.setText('⏸️')

    @property
    def current_frame(self):
        return self._current_frame

    @current_frame.setter
    def current_frame(self, value):
        value = int(value)
        if 0 <= value <= self._last_frame:
            self._current_frame = value
        else:
            self._current_frame = 0
