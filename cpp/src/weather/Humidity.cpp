#include "weather/Humidity.h"
#include "hdf5_utility.h"

namespace omega {

    bool Humidity::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "source", static_cast<int>(this->source_));
        omega::add_dataset_to_group(parent_group, "humidity", this->humidity_);
        return true;
    }

    Humidity Humidity::from_hdf5(hdf5::node::Group &parent_group) {
        Humidity humidity;

        int source;
        omega::read_attribute(parent_group, "source", source);
        humidity.source_ = VVMWeatherSource(source);
        omega::read_dataset(parent_group, "humidity", humidity.humidity_);

        return humidity;
    }
}
