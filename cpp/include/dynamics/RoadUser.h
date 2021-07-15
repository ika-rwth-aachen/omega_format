#ifndef ROADUSER_H
#define ROADUSER_H

#include <iostream>
#include <vector>
#include <h5cpp/hdf5.hpp>

#include <dynamics/BoundingBox.h>
#include <dynamics/Trajectory.h>
#include <dynamics/VehicleLights.h>

#include "reference_types.h"

using std::vector;
using std::endl;

enum inDTypes {
    car = 0,
    truck_bus = 1,
    bicycle = 2,
    pedestrian = 3
};

// miscObject uses the same roadUser class
class RoadUser {

    // general parameters
    int id;
    int birthStamp;
    int finalFrame;
    float time_step_length_in_sec;
    int numFrames;

    inDTypes inDType;

    void setInDType(std::string inDString);

    std::map<inDTypes, VVMRoadUserType> typeFrominDType{
            {inDTypes::car,        VVMRoadUserType::CAR},
            {inDTypes::truck_bus,  VVMRoadUserType::TRUCK},
            {inDTypes::bicycle,    VVMRoadUserType::BICYCLE},
            {inDTypes::pedestrian, VVMRoadUserType::PEDESTRIAN}
    };

    std::map<inDTypes, VVMRoadUserSubTypeGeneral> subTypeFrominDType{
            {inDTypes::car,        VVMRoadUserSubTypeGeneral::REGULAR},
            {inDTypes::truck_bus,  VVMRoadUserSubTypeGeneral::REGULAR},
            {inDTypes::bicycle,    VVMRoadUserSubTypeGeneral::REGULAR},
            {inDTypes::pedestrian, VVMRoadUserSubTypeGeneral::REGULAR}
    };

    // hard-coded default heights
    std::map<inDTypes, double> heightFrominDType{
            {inDTypes::car,        1.5},
            {inDTypes::truck_bus,  3.5},
            {inDTypes::bicycle,    1.8},
            {inDTypes::pedestrian, 1.75}
    };

    // hard-coded default lengths
    std::map<inDTypes, double> lengthFrominDType{
            {inDTypes::car,        0.0},  // not used
            {inDTypes::truck_bus,  0.0},  // not used
            {inDTypes::bicycle,    1.8},
            {inDTypes::pedestrian, 0.5}
    };

    // hard-coded default widths
    std::map<inDTypes, double> widthFrominDType{
            {inDTypes::car,        0.0},  // not used
            {inDTypes::truck_bus,  0.0},  // not used
            {inDTypes::bicycle,    0.8},
            {inDTypes::pedestrian, 0.5}
    };


public:

    // general parameters to be written to HDF5
    bool isDataRecorder;
    VVMRoadUserType numericalType;
    VVMRoadUserSubTypeGeneral numericalSubType;
    int connectedTo;

    BoundingBox bb;
    Trajectory tr;
    VehicleLights vl;

    // constructors
    RoadUser();

    RoadUser(int id,
             int birthStamp, int finalFrame,
             double width,
             double length,
             std::string inDTypeString,
             float time_step_length_in_sec,
             int lifetime);

    // getter
    int getId() const;

    int getInitialFrame() const;

    int getFinalFrame() const;

    int getNumFrames() const;

    // hdf5
    void to_hdf5(hdf5::node::Group &parent_group);
    static RoadUser from_hdf5(hdf5::node::Group parent_group);

    float getTime_step_length_in_sec() const;

private:
    void setPropertiesFromInDType(std::string inDTypeString, double length, double width);
};

#endif
