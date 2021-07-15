#include "weather/Cloudiness.h"
#include "hdf5_utility.h"

namespace omega {

    bool Cloudiness::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "source", static_cast<int>(this->source_));
        omega::add_dataset_to_group(parent_group, "degree", this->degree_);
        return true;
    }

    Cloudiness Cloudiness::from_hdf5(hdf5::node::Group &parent_group) {
        Cloudiness cloudiness;

        int source;
        omega::read_attribute(parent_group, "source", source);
        cloudiness.source_ = VVMWeatherSource(source);
        omega::read_dataset(parent_group, "degree", cloudiness.degree_);

        return cloudiness;
    }
}
