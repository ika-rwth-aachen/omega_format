#ifndef OMEGA_CPP_GUSTOFWIND_H
#define OMEGA_CPP_GUSTOFWIND_H


#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

    class GustOfWind {
    private:
        std::vector<float> windSpeed_;
        std::vector<int> type_;
        VVMWeatherSource source_;

    public:
        bool to_hdf5(hdf5::node::Group &parent_group);

        static GustOfWind from_hdf5(hdf5::node::Group &parent_group);
    };
}

#endif //OMEGA_CPP_GUSTOFWIND_H
