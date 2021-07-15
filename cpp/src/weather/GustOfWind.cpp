#include "weather/GustOfWind.h"
#include "hdf5_utility.h"

namespace omega {

    bool GustOfWind::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "source", static_cast<int>(this->source_));
        omega::add_dataset_to_group(parent_group, "type", this->type_);
        omega::add_dataset_to_group(parent_group, "windSpeed", this->windSpeed_);
        return true;
    }

    GustOfWind GustOfWind::from_hdf5(hdf5::node::Group &parent_group) {
        GustOfWind gustOfWind;

        int source;
        omega::read_attribute(parent_group, "source", source);
        gustOfWind.source_ = VVMWeatherSource(source);
        omega::read_dataset(parent_group, "type", gustOfWind.type_);
        omega::read_dataset(parent_group, "windSpeed", gustOfWind.windSpeed_);

        return gustOfWind;
    }
}
