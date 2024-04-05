from pydantic.dataclasses import Field
import numpy as np
from h5py import Group

from .air_pressure import AirPressure
from .cloudiness import Cloudiness
from .gust_of_wind import GustOfWind
from .humidity import Humidity
from .precipitation import Precipitation
from .road_condition import RoadCondition
from .solar import Solar
from .temperature import Temperature
from .visibility import Visibility
from .wind import Wind
from ..reference_resolving import InputClassBase


class Weather(InputClassBase):
    weather_station_id: str = ""
    precipitation: Precipitation = Field(default_factory=Precipitation)
    visibility: Visibility = Field(default_factory=Visibility)
    road_condition: RoadCondition = Field(default_factory=RoadCondition)
    cloudiness: Cloudiness = Field(default_factory=Cloudiness)
    solar: Solar = Field(default_factory=Solar)
    temperature: Temperature = Field(default_factory=Temperature)
    wind: Wind = Field(default_factory=Wind)
    gust_of_wind: GustOfWind = Field(default_factory=GustOfWind)
    air_pressure: AirPressure = Field(default_factory=AirPressure)
    humidity: Humidity = Field(default_factory=Humidity)

    @classmethod
    def from_hdf5(cls, group: Group, validate: bool = True, legacy=None):
        func = cls if validate else cls.model_construct
        self = func(
            weather_station_id=str(group.attrs["weatherStationId"]),
            precipitation=Precipitation.from_hdf5(group['precipitation'], validate=validate),
            visibility=Visibility.from_hdf5(group['visibility'], validate=validate),
            road_condition=RoadCondition.from_hdf5(group['roadCondition'], validate=validate),
            cloudiness=Cloudiness.from_hdf5(group['cloudiness'], validate=validate),
            solar=Solar.from_hdf5(group['solar'], validate=validate),
            temperature=Temperature.from_hdf5(group['temperature'], validate=validate),
            wind=Wind.from_hdf5(group['wind'], validate=validate),
            gust_of_wind=GustOfWind.from_hdf5(group['gustOfWind'], validate=validate),
            air_pressure=AirPressure.from_hdf5(group['airPressure'], validate=validate),
            humidity=Humidity.from_hdf5(group['humidity'], validate=validate)
        )
        return self

    def to_hdf5(self, group: Group):
        group.attrs.create('weatherStationId', data=self.weather_station_id)

        self.precipitation.to_hdf5(group.create_group('precipitation'))
        self.visibility.to_hdf5(group.create_group('visibility'))
        self.road_condition.to_hdf5(group.create_group('roadCondition'))
        self.cloudiness.to_hdf5(group.create_group('cloudiness'))
        self.solar.to_hdf5(group.create_group('solar'))
        self.temperature.to_hdf5(group.create_group('temperature'))
        self.wind.to_hdf5(group.create_group('wind'))
        self.gust_of_wind.to_hdf5(group.create_group('gustOfWind'))
        self.air_pressure.to_hdf5(group.create_group('airPressure'))
        self.humidity.to_hdf5(group.create_group('humidity'))

    def cut_to_timespan(self, birth, death):
        for k, v in vars(self).items():
            if isinstance(v, InputClassBase):
                for kk, vv in vars(v).items():
                    if isinstance(vv, np.ndarray):
                        setattr(v, kk, vv[birth:death+1])

    def get_weather_summary(self):
        summary = {
            'avg_temp': self.temperature.get_avg_temp(),
            'cloudy': self.cloudiness.is_cloudy,
            'foggy': self.humidity.is_foggy,
            'raining': self.precipitation.is_raining,
            'thunderstorm': self.precipitation.is_thunderstorm,
            'snowing': self.precipitation.is_snowing,
            'sunny': self.solar.is_sunny,
            'windy': self.wind.is_windy,
        }
        return summary
