#pragma once

#include <vector>
#include <h5cpp/hdf5.hpp>

class VehicleLights {
public:
    std::vector<int> indicatorRight;
    std::vector<int> indicatorLeft;
    std::vector<int> brakeLights;
    std::vector<int> headlights;
    std::vector<int> reversingLights;
    std::vector<int> blueLight;
    std::vector<int> orangeLight;

public:
    VehicleLights(size_t lifetime);

    // hdf5
    void to_hdf5(hdf5::node::Group &parent_group);
    static VehicleLights from_hdf5(hdf5::node::Group &parent_group);
};

