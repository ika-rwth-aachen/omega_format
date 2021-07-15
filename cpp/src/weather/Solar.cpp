#include "weather/Solar.h"
#include "hdf5_utility.h"

namespace omega {

    bool Solar::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "source", static_cast<int>(this->source_));
        omega::add_dataset_to_group(parent_group, "diffSolarRadiation", this->diffSolarRadiation_);
        omega::add_dataset_to_group(parent_group, "longwaveDownRadiation", this->longwaveDownRadiation_);
        omega::add_dataset_to_group(parent_group, "solarHours", this->solarHours_);
        omega::add_dataset_to_group(parent_group, "solarIncomingRadiation", this->solarIncomingRadiation_);
        return true;
    }

    Solar Solar::from_hdf5(hdf5::node::Group &parent_group) {
        Solar solar;

        int source;
        omega::read_attribute(parent_group, "source", source);
        solar.source_ = VVMWeatherSource(source);
        omega::read_dataset(parent_group, "diffSolarRadiation", solar.diffSolarRadiation_);
        omega::read_dataset(parent_group, "longwaveDownRadiation", solar.longwaveDownRadiation_);
        omega::read_dataset(parent_group, "solarHours", solar.solarHours_);
        omega::read_dataset(parent_group, "solarIncomingRadiation", solar.solarIncomingRadiation_);

        return solar;
    }
}
