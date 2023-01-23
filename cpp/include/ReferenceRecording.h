#ifndef OMEGA_REFERENCE_RECORDING
#define OMEGA_REFERENCE_RECORDING

#include <vector>
#include <memory>
#include <map>
#include <weather/Weather.h>
#include <optional>

#include "road/Road.h"
#include "dynamics/RoadUser.h"
#include "dynamics/MiscObject.h"
#include "MetaData.h"

namespace omega {

    class ReferenceRecording {
    public:
        MetaData metaData_;
        Roads_Ptr roads_; ///< Buffer to store the hdf5 roads
        std::vector<float> timestamps_;
        std::list<RoadUser> roadUsers_;
        std::optional<Weather> weather_;
        std::optional<std::list<MiscObject>> miscObjects_;
        // states


    public:
        /**
         * Constructor to create the shared_pointer that have this class as a parent.
         */
        ReferenceRecording();

        /**
         * Will write the entire hdf5 data structure to a file.
         * @param map_output_path Path of the hdf5 file.
         * @return true if an error occurred, false otherwise.
         */
        bool to_hdf5(const std::string &output_path);

        static ReferenceRecording from_hdf5(const std::string &input_path);

    };

    typedef std::shared_ptr<ReferenceRecording> ReferenceRecording_Ptr;
}
#endif //OMEGA_REFERENCE_RECORDING
