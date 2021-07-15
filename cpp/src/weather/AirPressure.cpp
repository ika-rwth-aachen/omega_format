#include "weather/AirPressure.h"
#include "hdf5_utility.h"

namespace omega {

    bool AirPressure::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "source", static_cast<int>(this->source_));
        omega::add_dataset_to_group(parent_group, "airPressureNN", this->airPressureNN_);
        omega::add_dataset_to_group(parent_group, "airPressureZero", this->airPressureZero_);
        return true;
    }

    AirPressure AirPressure::from_hdf5(hdf5::node::Group &parent_group) {
        AirPressure airPressure;

        int source;
        omega::read_attribute(parent_group, "source", source);
        airPressure.source_ = VVMWeatherSource(source);
        omega::read_dataset(parent_group, "airPressureNN", airPressure.airPressureNN_);
        omega::read_dataset(parent_group, "airPressureZero", airPressure.airPressureZero_);

        return airPressure;
    }
}
