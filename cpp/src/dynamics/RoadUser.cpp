#include "dynamics/RoadUser.h"
#include "hdf5_utility.h"

RoadUser::RoadUser() : tr(0), vl(0) {

    this->numFrames = 0;
    this->birthStamp = 0;
    this->finalFrame = 0;
    this->time_step_length_in_sec = 0.0;
    this->id = "RU0";
    this->isDataRecorder = false;
    this->connectedTo = "RU-1";
    this->attachedTo = "RU-1";

    numericalType = VVMRoadUserType::REGULAR;
    numericalSubType = VVMRoadUserSubTypeGeneral::REGULAR;
}

RoadUser::RoadUser(std::string id,
                   int birthStamp, int finalFrame,
                   double width,
                   double length,
                   std::string inDTypeString,
                   float time_step_length_in_sec,
                   int lifetime) :
        id(id),
        birthStamp(birthStamp),
        finalFrame(finalFrame),
        time_step_length_in_sec(time_step_length_in_sec),
        numFrames(lifetime),
        tr(size_t(lifetime)),
        vl(size_t(lifetime)) {

    this->setPropertiesFromInDType(inDTypeString, length, width);
    this->connectedTo = 'RU-1';
    this->attachedTo = 'RU-1';
    this->isDataRecorder = false;
}

float RoadUser::getTime_step_length_in_sec() const {
    return time_step_length_in_sec;
}

void RoadUser::setInDType(std::string inDString) {
    if (inDString.find("car") != std::string::npos) {
        this->inDType = inDTypes::car;
        return;
    }
    if (inDString.find("truck_bus") != std::string::npos) {
        this->inDType = inDTypes::truck_bus;
        return;
    }
    if (inDString.find("bicycle") != std::string::npos) {
        this->inDType = inDTypes::bicycle;
        return;
    }
    if (inDString.find("pedestrian") != std::string::npos) {
        this->inDType = inDTypes::pedestrian;
        return;
    }
    std::cerr << "inDType of roadUser could not be determined." << std::endl;
}

void RoadUser::setPropertiesFromInDType(std::string inDTypeString, double length, double width) {
    this->setInDType(inDTypeString);

    this->numericalType = this->typeFrominDType[this->inDType];
    this->numericalSubType = this->subTypeFrominDType[this->inDType];
    bb.setHeight(this->heightFrominDType[this->inDType]);

    if (this->inDType == inDTypes::car || this->inDType == inDTypes::truck_bus) {
        bb.setLength(length);
        bb.setWidth(width);
    } else {
        bb.setWidth(this->widthFrominDType[this->inDType]);
        bb.setLength(this->lengthFrominDType[this->inDType]);
    }
}

std::string RoadUser::getId() const {
    return this->id;
}

int RoadUser::getInitialFrame() const {
    return this->birthStamp;
}

int RoadUser::getFinalFrame() const {
    return this->finalFrame;
}

int RoadUser::getNumFrames() const {
    return this->numFrames;
}

void RoadUser::to_hdf5(hdf5::node::Group &parent_group) {
    // maybe use some assertions before writing

    // Writing the hdf group to a group with id as name
    hdf5::node::Group ru_group(parent_group.create_group(std::to_string(this->id)));

    bb.to_hdf5(ru_group);
    tr.to_hdf5(ru_group);
    vl.to_hdf5(ru_group);

    int type = static_cast<int>(this->numericalType);
    int subtype = static_cast<int>(this->numericalSubType);
    omega::add_attribute_to_group(ru_group, "type", type);
    omega::add_attribute_to_group(ru_group, "subtype", subtype);

    omega::add_attribute_to_group(ru_group, "connectedTo", this->connectedTo);
    omega::add_attribute_to_group(ru_group, "attachedTo", this->attachedTo);
    omega::add_attribute_to_group(ru_group, "birthStamp", this->getInitialFrame());
    omega::add_attribute_to_group(ru_group, "isDataRecorder", this->isDataRecorder);
}

RoadUser RoadUser::from_hdf5(hdf5::node::Group parent_group) {
    RoadUser road_user;

    int type, subtype;
    omega::read_attribute(parent_group, "type", type);
    omega::read_attribute(parent_group, "subtype", subtype);
    road_user.numericalType = VVMRoadUserType(type);
    road_user.numericalSubType = VVMRoadUserSubTypeGeneral(subtype);

    road_user.id = omega::get_group_id(parent_group);
    omega::read_attribute(parent_group, "connectedTo", road_user.connectedTo);
    omega::read_attribute(parent_group, "attachedTo", road_user.attachedTo);
    omega::read_attribute(parent_group, "birthStamp", road_user.birthStamp);
    omega::read_attribute(parent_group, "isDataRecorder", road_user.isDataRecorder);

    hdf5::node::Group bound_box_group = parent_group.get_group("boundBox");
    hdf5::node::Group trajectory_group = parent_group.get_group("trajectory");
    hdf5::node::Group vehicle_lights_group = parent_group.get_group("vehicleLights");
    road_user.bb = BoundingBox::from_hdf5(bound_box_group);
    road_user.tr = Trajectory::from_hdf5(trajectory_group);
    road_user.vl = VehicleLights::from_hdf5(vehicle_lights_group);

    return road_user;
}


// overload << operator to output one roadUser (used for debug)
std::ostream &operator<<(std::ostream &os, const RoadUser &ru) {
    os << "Road user nr.:    " << ru.getId() << "\n";
    os << "-> initial frame: " << ru.getInitialFrame() << "\n";
    os << "-> final frame:   " << ru.getFinalFrame() << "\n";
    os << "-> lifetime:      " << ru.getFinalFrame() - ru.getInitialFrame() + 1 << "\n";
    os << endl;
    return os;
}
