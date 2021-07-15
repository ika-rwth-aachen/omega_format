#ifndef OMEGA_CPP_PRECIPITATION_H
#define OMEGA_CPP_PRECIPITATION_H


#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

    class Precipitation {
    private:
        std::vector<float> amountHourly_;
        std::vector<float> amountMinute_;
        std::vector<float> newSnowDepth_;
        std::vector<float> snowDepth_;
        std::vector<int> type_;
        VVMWeatherSource source_;

    public:
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Precipitation from_hdf5(hdf5::node::Group &parent_group);
    };
}

#endif //OMEGA_CPP_PRECIPITATION_H
