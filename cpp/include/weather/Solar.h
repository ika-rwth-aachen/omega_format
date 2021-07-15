#ifndef OMEGA_CPP_SOLAR_H
#define OMEGA_CPP_SOLAR_H


#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

    class Solar {
    private:
        std::vector<float> diffSolarRadiation_;
        std::vector<float> longwaveDownRadiation_;
        std::vector<float> solarHours_;
        std::vector<float> solarIncomingRadiation_;
        VVMWeatherSource source_;


    public:
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Solar from_hdf5(hdf5::node::Group &parent_group);
    };
}

#endif //OMEGA_CPP_SOLAR_H
