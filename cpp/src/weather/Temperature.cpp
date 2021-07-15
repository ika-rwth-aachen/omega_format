#include "weather/Temperature.h"
#include "hdf5_utility.h"

namespace omega {

    bool Temperature::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "source", static_cast<int>(this->source_));
        omega::add_dataset_to_group(parent_group, "airTemp", this->airTemp_);
        omega::add_dataset_to_group(parent_group, "airTemp5cm", this->airTemp5cm_);
        omega::add_dataset_to_group(parent_group, "groundTemp", this->groundTemp_);
        return true;
    }

    Temperature Temperature::from_hdf5(hdf5::node::Group &parent_group) {
        Temperature temperature;

        int source;
        omega::read_attribute(parent_group, "source", source);
        temperature.source_ = VVMWeatherSource(source);
        omega::read_dataset(parent_group, "airTemp", temperature.airTemp_);
        omega::read_dataset(parent_group, "airTemp5cm", temperature.airTemp5cm_);
        omega::read_dataset(parent_group, "groundTemp", temperature.groundTemp_);

        return temperature;
    }
}
