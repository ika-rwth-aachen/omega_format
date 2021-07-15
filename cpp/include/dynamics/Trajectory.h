#pragma once

#include <vector>
#include <h5cpp/hdf5.hpp>

class Trajectory {
public:
    // positions, velocities, accelerations; indices: 0=X, 1=Y, 2=Z
    std::vector<float> positions[3];
    std::vector<float> velocities[3];
    std::vector<float> accelerations[3];

    // vel, acc in longitudinal/lateral direction
    std::vector<float> lonVelocity;
    std::vector<float> latVelocity;
    std::vector<float> lonAcceleration;
    std::vector<float> latAcceleration;

    // angles, indices: 0=heading, 1=pitch, 2=roll
    std::vector<float> angles[3];
    std::vector<float> angularVels[3];

public:
    // further functions
    void computeAngularVel(float time_step_length_in_sec);

    static float clampAngleDiff(float angleDiff);

public:
    Trajectory(size_t lifetime);

    void to_hdf5(hdf5::node::Group &parent_group);
    static Trajectory from_hdf5(hdf5::node::Group &parent_group);
};
