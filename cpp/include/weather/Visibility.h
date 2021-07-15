#ifndef OMEGA_CPP_VISIBILITY_H
#define OMEGA_CPP_VISIBILITY_H


#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

    class Visibility {
    private:
        std::vector<float> visibility_;
        VVMWeatherSource source_;

    public:
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Visibility from_hdf5(hdf5::node::Group &parent_group);
    };
}

#endif //OMEGA_CPP_VISIBILITY_H
