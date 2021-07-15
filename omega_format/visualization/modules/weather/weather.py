from pathlib import Path

from PyQt5.QtGui import QPen, QBrush, QColor, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from ..base import VisualizationModule, SnippetContainer, VisualizationModuleType
from ...pyqt_helper import *
from ....road import Lane, Sign, Border, LateralMarking, FlatMarking, Boundary
from ....enums import ReferenceTypes
from ....weather import Weather
import pyqtgraph as pg


class VisualizeWeather(VisualizationModule):
    def __init__(self, **kwargs):
        super().__init__('Weather', **kwargs)
        self.requires = [SnippetContainer.REQ_REFERENCE]
        self.type = VisualizationModuleType.HIDE

    def visualize_statics(self, snip, visualizer):
        items = []

        if snip.reference.weather is None:
            visualizer.weather_degree_lbl.setText('weather not available')
        else:
            weather_dict = snip.reference.weather.get_weather_summary()

            avg_temp = weather_dict['avg_temp']
            text = f'temperature: {avg_temp:.1f}°C'
            visualizer.weather_degree_lbl.setText(text)

            base_path = str(Path(__file__).parent.absolute())

            if weather_dict['sunny'] == weather_dict['cloudy']:
                icon_name = 'cloud_sun'
                self._visualize_weather_icon(visualizer, base_path, icon_name)
            elif weather_dict['sunny']:
                icon_name = 'sun'
                self._visualize_weather_icon(visualizer, base_path, icon_name)
            elif weather_dict['cloudy']:
                icon_name = 'cloud'
                self._visualize_weather_icon(visualizer, base_path, icon_name)

            if weather_dict['raining']:
                icon_name = 'rain'
                self._visualize_weather_icon(visualizer, base_path, icon_name)
            elif weather_dict['thunderstorm']:
                icon_name = 'thunderstorm'
                self._visualize_weather_icon(visualizer, base_path, icon_name)
            elif weather_dict['snowing']:
                icon_name = 'snow'
                self._visualize_weather_icon(visualizer, base_path, icon_name)

            if weather_dict['foggy']:
                icon_name = 'fog'
                self._visualize_weather_icon(visualizer, base_path, icon_name)

            if weather_dict['windy']:
                icon_name = 'wind'
                self._visualize_weather_icon(visualizer, base_path, icon_name)

        return items

    def _visualize_weather_icon(self, visualizer, base_path: str, icon_name: str):
        img_path = base_path + f'/icons/{icon_name}.png'
        img = QPixmap(img_path)
        img = img.scaled(50, 50, aspectRatioMode=Qt.KeepAspectRatio)

        lbl = QLabel()
        lbl.setPixmap(img)
        visualizer.weather_h_layout.addWidget(lbl)
