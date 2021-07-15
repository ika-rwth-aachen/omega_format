#ifndef OMEGA_CPP_TEMPERATURE_H
#define OMEGA_CPP_TEMPERATURE_H


#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

    class Temperature {
    private:
        std::vector<float> airTemp_;
        std::vector<float> airTemp5cm_;
        std::vector<float> groundTemp_;
        std::vector<float> solarIncomingRadiations_;
        VVMWeatherSource source_;

    public:
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Temperature from_hdf5(hdf5::node::Group &parent_group);
    };
}

#endif //OMEGA_CPP_TEMPERATURE_H
