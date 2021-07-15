#ifndef OMEGA_CPP_HUMIDITY_H
#define OMEGA_CPP_HUMIDITY_H


#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

    class Humidity {
    private:
        std::vector<float> humidity_;
        VVMWeatherSource source_;

    public:
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Humidity from_hdf5(hdf5::node::Group &parent_group);
    };
}


#endif //OMEGA_CPP_HUMIDITY_H
