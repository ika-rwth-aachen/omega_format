#include "weather/Wind.h"
#include "hdf5_utility.h"

namespace omega {

    bool Wind::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "source", static_cast<int>(this->source_));
        omega::add_dataset_to_group(parent_group, "windSpeed", this->windSpeed_);
        omega::add_dataset_to_group(parent_group, "windDirection", this->windDirection_);
        omega::add_dataset_to_group(parent_group, "type", this->type_);
        return true;
    }

    Wind Wind::from_hdf5(hdf5::node::Group &parent_group) {
        Wind wind;

        int source;
        omega::read_attribute(parent_group, "source", source);
        wind.source_ = VVMWeatherSource(source);
        omega::read_dataset(parent_group, "windSpeed", wind.windSpeed_);
        omega::read_dataset(parent_group, "windDirection", wind.windDirection_);
        omega::read_dataset(parent_group, "type", wind.type_);

        return wind;
    }
}
