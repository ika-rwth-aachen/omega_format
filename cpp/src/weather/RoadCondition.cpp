#include "weather/RoadCondition.h"
#include "hdf5_utility.h"

namespace omega {

    bool RoadCondition::to_hdf5(hdf5::node::Group &parent_group) {
        omega::add_attribute_to_group(parent_group, "source", static_cast<int>(this->source_));
        omega::add_dataset_to_group(parent_group, "maintenanceStatus", this->maintenanceStatus_);
        omega::add_dataset_to_group(parent_group, "spray", this->spray_);
        omega::add_dataset_to_group(parent_group, "surfaceCondition", this->surfaceCondition_);
        return true;
    }

    RoadCondition RoadCondition::from_hdf5(hdf5::node::Group &parent_group) {
        RoadCondition roadCondition;

        int source;
        omega::read_attribute(parent_group, "source", source);
        roadCondition.source_ = VVMWeatherSource(source);
        omega::read_dataset(parent_group, "maintenanceStatus", roadCondition.maintenanceStatus_);
        omega::read_dataset(parent_group, "spray", roadCondition.spray_);
        omega::read_dataset(parent_group, "surfaceCondition", roadCondition.surfaceCondition_);

        return roadCondition;
    }
}
