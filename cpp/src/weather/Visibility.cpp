#include "weather/Visibility.h"
#include "hdf5_utility.h"

namespace omega {

    bool Visibility::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "source", static_cast<int>(this->source_));
        omega::add_dataset_to_group(parent_group, "visibility", this->visibility_);
        return true;
    }

    Visibility Visibility::from_hdf5(hdf5::node::Group &parent_group) {
        Visibility visibility;

        int source;
        omega::read_attribute(parent_group, "source", source);
        visibility.source_ = VVMWeatherSource(source);
        omega::read_dataset(parent_group, "visibility", visibility.visibility_);

        return visibility;
    }
}
