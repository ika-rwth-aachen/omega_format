#ifndef OMEGA_CPP_WEATHER_H
#define OMEGA_CPP_WEATHER_H

#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>
#include "weather/Precipitation.h"
#include "weather/Visibility.h"
#include "weather/RoadCondition.h"
#include "weather/Cloudiness.h"
#include "weather/Solar.h"
#include "weather/Temperature.h"
#include "weather/Wind.h"
#include "weather/GustOfWind.h"
#include "weather/AirPressure.h"
#include "weather/Humidity.h"


#include "vvm_definitions.h"

namespace omega {

    class Weather {
    private:
        int weather_station_id;
        Precipitation precipitation_;
        Visibility visibility_;
        RoadCondition roadCondition_;
        Cloudiness cloudiness_;
        Solar solar_;
        Temperature temperature_;
        Wind wind_;
        GustOfWind gustOfWind_;
        AirPressure airPressure_;
        Humidity humidity_;

    public:
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Weather from_hdf5(hdf5::node::Group &parent_group);
    };
}
#endif //OMEGA_CPP_WEATHER_H
