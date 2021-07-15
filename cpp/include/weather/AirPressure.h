#ifndef OMEGA_CPP_AIRPRESSURE_H
#define OMEGA_CPP_AIRPRESSURE_H


#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

    class AirPressure {
    private:
        std::vector<float> airPressureNN_;
        std::vector<float> airPressureZero_;
        VVMWeatherSource source_;

    public:
        bool to_hdf5(hdf5::node::Group &parent_group);

        static AirPressure from_hdf5(hdf5::node::Group &parent_group);
    };
}


#endif //OMEGA_CPP_AIRPRESSURE_H
