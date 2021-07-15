#ifndef MISCOBJECT_H
#define MISCOBJECT_H

#include <vector>
#include <string>

#include <h5cpp/hdf5.hpp>
#include <dynamics/BoundingBox.h>
#include <dynamics/Trajectory.h>

#include "vvm_definitions.h"

namespace omega {

class MiscObject {
    private:
        int id;
        int birthStamp;
        VVMMiscObjectType type_;
        VVMMiscObjectSubType subtype_;
        BoundingBox bb;
        Trajectory tr;
    public:
        MiscObject();

        bool to_hdf5(hdf5::node::Group &parent_group);

        static MiscObject from_hdf5(hdf5::node::Group &parent_group);
    };
}


#endif
