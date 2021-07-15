#ifndef OMEGA_CPP_ROADCONDITION_H
#define OMEGA_CPP_ROADCONDITION_H

#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

    class RoadCondition {
    private:
        std::vector<int> maintenanceStatus_;
        std::vector<int> spray_;
        std::vector<int> surfaceCondition_;
        VVMWeatherSource source_;

    public:
        bool to_hdf5(hdf5::node::Group &parent_group);

        static RoadCondition from_hdf5(hdf5::node::Group &parent_group);
    };
}

#endif //OMEGA_CPP_ROADCONDITION_H
