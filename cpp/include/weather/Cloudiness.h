#ifndef OMEGA_CPP_CLOUDINESS_H
#define OMEGA_CPP_CLOUDINESS_H

#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

    class Cloudiness {
    private:
        std::vector<float> degree_;
        VVMWeatherSource source_;

    public:
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Cloudiness from_hdf5(hdf5::node::Group &parent_group);
    };
}

#endif //OMEGA_CPP_CLOUDINESS_H
