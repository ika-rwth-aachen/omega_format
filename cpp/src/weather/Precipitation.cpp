#include "weather/Precipitation.h"
#include "hdf5_utility.h"

namespace omega {

    bool Precipitation::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "source", static_cast<int>(this->source_));
        omega::add_dataset_to_group(parent_group, "amountHourly", this->amountHourly_);
        omega::add_dataset_to_group(parent_group, "amountMinute", this->amountMinute_);
        omega::add_dataset_to_group(parent_group, "newSnowDepth", this->newSnowDepth_);
        omega::add_dataset_to_group(parent_group, "snowDepth", this->snowDepth_);
        omega::add_dataset_to_group(parent_group, "type", this->type_);
        return true;
    }

    Precipitation Precipitation::from_hdf5(hdf5::node::Group &parent_group) {
        Precipitation precipitation;

        int source;
        omega::read_attribute(parent_group, "source", source);
        precipitation.source_ = VVMWeatherSource(source);
        omega::read_dataset(parent_group, "amountHourly", precipitation.amountHourly_);
        omega::read_dataset(parent_group, "amountMinute", precipitation.amountMinute_);
        omega::read_dataset(parent_group, "newSnowDepth", precipitation.newSnowDepth_);
        omega::read_dataset(parent_group, "snowDepth", precipitation.snowDepth_);
        omega::read_dataset(parent_group, "type", precipitation.type_);

        return precipitation;
    }
}
