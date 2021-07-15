#include <dynamics/VehicleLights.h>
#include "reference_types.h"
#include "hdf5_utility.h"

VehicleLights::VehicleLights(size_t lifetime) {
    this->indicatorLeft.resize(lifetime, static_cast<int>(VVMRoadUserVehicleLights::UNKNOWN));
    this->indicatorRight.resize(lifetime, static_cast<int>(VVMRoadUserVehicleLights::UNKNOWN));
    this->brakeLights.resize(lifetime, static_cast<int>(VVMRoadUserVehicleLights::UNKNOWN));
    this->reversingLights.resize(lifetime, static_cast<int>(VVMRoadUserVehicleLights::UNKNOWN));
    this->blueLight.resize(lifetime, static_cast<int>(VVMRoadUserVehicleLights::UNKNOWN));
    this->headlights.resize(lifetime, static_cast<int>(VVMRoadUserVehicleLights::UNKNOWN));
}

void VehicleLights::to_hdf5(hdf5::node::Group &parent_group) {
    // Writing the hdf group to a group with id as name
    hdf5::node::Group vehicle_lights_group(parent_group.create_group("vehicleLights"));

    omega::add_dataset_to_group(vehicle_lights_group, "indicatorLeft", this->indicatorLeft);
    omega::add_dataset_to_group(vehicle_lights_group, "indicatorRight", this->indicatorRight);
    omega::add_dataset_to_group(vehicle_lights_group, "brakeLights", this->brakeLights);
    omega::add_dataset_to_group(vehicle_lights_group, "reversingLights", this->reversingLights);
    omega::add_dataset_to_group(vehicle_lights_group, "blueLight", this->blueLight);
    omega::add_dataset_to_group(vehicle_lights_group, "headlights", this->headlights);
}

VehicleLights VehicleLights::from_hdf5(hdf5::node::Group &parent_group) {
    VehicleLights vehicleLights(0);

    omega::read_dataset(parent_group, "indicatorLeft",vehicleLights.indicatorLeft);
    omega::read_dataset(parent_group, "indicatorRight",vehicleLights.indicatorRight);
    omega::read_dataset(parent_group, "brakeLights",vehicleLights.brakeLights);
    omega::read_dataset(parent_group, "reversingLights",vehicleLights.reversingLights);
    omega::read_dataset(parent_group, "blueLight",vehicleLights.blueLight);
    omega::read_dataset(parent_group, "headlights",vehicleLights.headlights);

    return vehicleLights;
}
