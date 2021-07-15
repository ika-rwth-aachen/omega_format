#include "weather/Weather.h"
#include "hdf5_utility.h"

namespace omega {

    bool Weather::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "weatherStationId", this->weather_station_id);

        hdf5::node::Group precipitation_group = parent_group.create_group("precipitation");
        hdf5::node::Group visibility_group = parent_group.create_group("visibility");
        hdf5::node::Group roadCondition_group = parent_group.create_group("roadCondition");
        hdf5::node::Group cloudiness_group = parent_group.create_group("cloudiness");
        hdf5::node::Group solar_group = parent_group.create_group("solar");
        hdf5::node::Group temperature_group = parent_group.create_group("temperature");
        hdf5::node::Group wind_group = parent_group.create_group("wind");
        hdf5::node::Group gustOfWind_group = parent_group.create_group("gustOfWind");
        hdf5::node::Group airPressure_group = parent_group.create_group("airPressure");
        hdf5::node::Group humidity_group = parent_group.create_group("humidity");

        this->precipitation_.to_hdf5(precipitation_group);
        this->visibility_.to_hdf5(visibility_group);
        this->roadCondition_.to_hdf5(roadCondition_group);
        this->cloudiness_.to_hdf5(cloudiness_group);
        this->solar_.to_hdf5(solar_group);
        this->temperature_.to_hdf5(temperature_group);
        this->wind_.to_hdf5(wind_group);
        this->gustOfWind_.to_hdf5(gustOfWind_group);
        this->airPressure_.to_hdf5(airPressure_group);
        this->humidity_.to_hdf5(humidity_group);

        return true;
    }

    Weather Weather::from_hdf5(hdf5::node::Group &parent_group) {
        Weather weather;

        omega::read_attribute(parent_group, "weatherStationId", weather.weather_station_id);

        hdf5::node::Group precipitation_group = parent_group.get_group("precipitation");
        hdf5::node::Group visibility_group = parent_group.get_group("visibility");
        //hdf5::node::Group roadCondition_group =  parent_group.get_group("roadCondition");
        hdf5::node::Group cloudiness_group = parent_group.get_group("cloudiness");
        hdf5::node::Group solar_group = parent_group.get_group("solar");
        hdf5::node::Group temperature_group = parent_group.get_group("temperature");
        hdf5::node::Group wind_group = parent_group.get_group("wind");
        hdf5::node::Group gustOfWind_group = parent_group.get_group("gustOfWind");
        hdf5::node::Group airPressure_group = parent_group.get_group("airPressure");
        hdf5::node::Group humidity_group = parent_group.get_group("humidity");

        weather.precipitation_ = Precipitation::from_hdf5(precipitation_group);
        weather.visibility_ = Visibility::from_hdf5(visibility_group);
        //weather.roadCondition_ = RoadCondition::from_hdf5(roadCondition_group);
        weather.cloudiness_ = Cloudiness::from_hdf5(cloudiness_group);
        weather.solar_ = Solar::from_hdf5(solar_group);
        weather.temperature_ = Temperature::from_hdf5(temperature_group);
        weather.wind_ = Wind::from_hdf5(wind_group);
        weather.gustOfWind_ = GustOfWind::from_hdf5(gustOfWind_group);
        weather.airPressure_ = AirPressure::from_hdf5(airPressure_group);
        weather.humidity_ = Humidity::from_hdf5(humidity_group);

        return weather;
    }
}