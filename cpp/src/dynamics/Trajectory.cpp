#include "dynamics/Trajectory.h"
#include "hdf5_utility.h"

Trajectory::Trajectory(size_t lifetime) {
    for (short i = 0; i < 3; ++i) {
        this->positions[i].resize(lifetime, 0.0);
        this->velocities[i].resize(lifetime, 0.0);
        this->accelerations[i].resize(lifetime, 0.0);
        this->angles[i].resize(lifetime, 0.0);
        this->angularVels[i].resize(lifetime, 0.0);
    }
    this->lonVelocity.resize(lifetime, 0.0);
    this->latVelocity.resize(lifetime, 0.0);
    this->lonAcceleration.resize(lifetime, 0.0);
    this->latAcceleration.resize(lifetime, 0.0);
}


float Trajectory::clampAngleDiff(float angleDiff) {
    const float limit = 180.f;  // for both positive and negative angle differences
    while (angleDiff > limit) { angleDiff -= 360.f; }
    while (angleDiff <= -limit) { angleDiff += 360.f; }
    return angleDiff;
}


void Trajectory::computeAngularVel(float time_step_length_in_sec) {

    float currentHeading, currentPitch, currentRoll;
    float prevHeading, prevPitch, prevRoll;

    // Compute angular velocities by dividing the difference of two neighboring angles by the frameRate
    for (size_t i = 1; i < this->angularVels[0].size(); ++i) {

        currentHeading = this->angles[0][i];
        currentPitch = this->angles[1][i];
        currentRoll = this->angles[2][i];
        prevHeading = this->angles[0][i - 1];
        prevPitch = this->angles[1][i - 1];
        prevRoll = this->angles[2][i - 1];

        this->angularVels[0][i] = clampAngleDiff(currentHeading - prevHeading) / time_step_length_in_sec;
        this->angularVels[1][i] = clampAngleDiff(currentPitch - prevPitch) / time_step_length_in_sec;
        this->angularVels[2][i] = clampAngleDiff(currentRoll - prevRoll) / time_step_length_in_sec;
    }
    this->angularVels[0][0] = this->angularVels[0][1];
    this->angularVels[1][0] = this->angularVels[1][1];
    this->angularVels[2][0] = this->angularVels[2][1];
}

void Trajectory::to_hdf5(hdf5::node::Group &parent_group) {

    hdf5::node::Group trajectory_group(parent_group.create_group("trajectory"));

    omega::add_dataset_to_group(trajectory_group, "posX", this->positions[0]);
    omega::add_dataset_to_group(trajectory_group, "posY", this->positions[1]);
    omega::add_dataset_to_group(trajectory_group, "posZ", this->positions[2]);

    omega::add_dataset_to_group(trajectory_group, "velLongitudinal", this->lonVelocity);
    omega::add_dataset_to_group(trajectory_group, "velLateral", this->latVelocity);
    omega::add_dataset_to_group(trajectory_group, "velZ", this->velocities[2]);

    omega::add_dataset_to_group(trajectory_group, "accLongitudinal", this->lonAcceleration);
    omega::add_dataset_to_group(trajectory_group, "accLateral", this->latAcceleration);
    omega::add_dataset_to_group(trajectory_group, "accZ", this->accelerations[2]);

    omega::add_dataset_to_group(trajectory_group, "heading", this->angles[0]);
    omega::add_dataset_to_group(trajectory_group, "pitch", this->angles[1]);
    omega::add_dataset_to_group(trajectory_group, "roll", this->angles[2]);

    omega::add_dataset_to_group(trajectory_group, "headingDer", this->angularVels[0]);
    omega::add_dataset_to_group(trajectory_group, "pitchDer", this->angularVels[1]);
    omega::add_dataset_to_group(trajectory_group, "rollDer", this->angularVels[2]);

}

Trajectory Trajectory::from_hdf5(hdf5::node::Group &parent_group) {
    Trajectory trajectory(0);

    omega::read_dataset(parent_group, "posX", trajectory.positions[0]);
    omega::read_dataset(parent_group, "posY", trajectory.positions[1]);
    omega::read_dataset(parent_group, "posZ", trajectory.positions[2]);

    omega::read_dataset(parent_group, "velLongitudinal", trajectory.lonVelocity);
    omega::read_dataset(parent_group, "velLateral", trajectory.latVelocity);
    omega::read_dataset(parent_group, "velZ", trajectory.velocities[2]);

    omega::read_dataset(parent_group, "accLongitudinal", trajectory.lonAcceleration);
    omega::read_dataset(parent_group, "accLateral", trajectory.latAcceleration);
    omega::read_dataset(parent_group, "accZ", trajectory.accelerations[2]);

    omega::read_dataset(parent_group, "heading", trajectory.angles[0]);
    omega::read_dataset(parent_group, "pitch", trajectory.angles[1]);
    omega::read_dataset(parent_group, "roll", trajectory.angles[2]);

    omega::read_dataset(parent_group, "headingDer", trajectory.angularVels[0]);
    omega::read_dataset(parent_group, "pitchDer", trajectory.angularVels[1]);
    omega::read_dataset(parent_group, "rollDer", trajectory.angularVels[2]);

    return trajectory;
}

