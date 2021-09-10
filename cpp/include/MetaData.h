#ifndef OMEGA_METADATA_H
#define OMEGA_METADATA_H

#include <h5cpp/hdf5.hpp>

#include <vector>
#include <string>

#include "reference_types.h"

namespace omega {
    class MetaData {
    public:
        std::string daytime;
        std::string formatVersion;
        VVMRecorderNumber recorderNumber;
        int recordingNumber;

        double refPointLong;
        double refPointLat;

        bool naturalBehavior;
        bool naturalExposure;

        std::string topLevelConverterVersion;
        std::string roadUserConverterVersion;
        std::string roadConverterVersion;
        std::string weatherConverterVersion;
        std::string stateConverterVersion;
        std::string miscObjectConverterVersion;
        std::string customInformation;

        int referenceModality;

    public:
        // default constructor creates "empty" object
        MetaData();

        // hdf5
        void to_hdf5(hdf5::node::Group &parent_group);

        static MetaData from_hdf5(hdf5::node::Group &parent_group);
    };

}
#endif
