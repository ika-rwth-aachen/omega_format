#include "road/Road.h"

#include "road/RoadObject.h"
#include "road/StructuralObject.h"
#include "road/Sign.h"
#include "road/LateralMarking.h"
#include "road/Lane.h"
#include "road/Border.h"

#include "hdf5_utility.h"

namespace omega {

    Road::Road() {
        this->lanes_ = std::make_shared<Lanes>();
        this->borders_ = std::make_shared<Borders>();
        this->lateral_markings_ = std::make_shared<LateralMarkings>();
        this->signs_ = std::make_shared<Signs>();
        this->road_objects_ = std::make_shared<RoadObjects>();
        this->structural_objects_ = std::make_shared<StructuralObjects>();
    }

    bool Road::to_hdf5(hdf5::node::Group &parent_group) {
        try {
            // Writing to the hdf5 file
            hdf5::node::Group hdf5_group_current_road(parent_group.create_group(std::to_string(this->road_id_)));
            omega::add_attribute_to_group(hdf5_group_current_road, "name", this->road_name_);
            omega::add_attribute_to_group(hdf5_group_current_road, "location", static_cast<int>(this->road_location_));
            omega::add_attribute_to_group(hdf5_group_current_road, "numLanes", this->getNumberOfLanes());

            // Writing all children borders
            auto hdf5_group_current_road_border = hdf5::node::Group(hdf5_group_current_road.create_group("border"));
            for (const auto &border: *this->borders_) {
                border->to_hdf5(hdf5_group_current_road_border);
            }

            // Writing children lanes to the hdf5 file
            hdf5::node::Group hdf5_ground_current_road_lane(hdf5_group_current_road.create_group("lane"));
            for (const auto &lane:*this->lanes_) {
                lane->to_hdf5(hdf5_ground_current_road_lane);
            }

            // Writing children lateral markings to the hdf5 file
            hdf5::node::Group hdf5_ground_current_lateral_markings(
                    hdf5_group_current_road.create_group("lateralMarking"));
            for (const auto &lateral_marking:*this->lateral_markings_) {
                lateral_marking->to_hdf5(hdf5_ground_current_lateral_markings);
            }

            // Writing children lateral markings to the hdf5 file
            hdf5::node::Group hdf5_ground_current_signs(hdf5_group_current_road.create_group("sign"));
            for (const auto &sign:*this->signs_) {
                sign->to_hdf5(hdf5_ground_current_signs);
            }

            // Writing road objects to the hdf5 file
            hdf5::node::Group hdf5_ground_current_road_objects(hdf5_group_current_road.create_group("roadObject"));
            for (const auto &road_object:*this->road_objects_) {
                road_object->to_hdf5(hdf5_ground_current_road_objects);
            }

            // Writing structural objects to the hdf5 file
            hdf5::node::Group hdf5_ground_current_structural_objects(
                    hdf5_group_current_road.create_group("structuralObject"));
            for (const auto &structural_object:*this->structural_objects_) {
                structural_object->to_hdf5(hdf5_ground_current_structural_objects);
            }
            return true;
        } catch (std::exception &e) {

            return false;
        }
    }

    Road Road::from_hdf5(hdf5::node::Group &parent_group) {
        Road road;

        road.road_id_ = omega::get_group_id(parent_group);

        hdf5::node::Group border_group = parent_group.get_group("border");
        hdf5::node::Group lane_group = parent_group.get_group("lane");
        hdf5::node::Group lateralMarking_group = parent_group.get_group("lateralMarking");
        hdf5::node::Group roadObject_group = parent_group.get_group("roadObject");
        hdf5::node::Group sign_group = parent_group.get_group("sign");
        hdf5::node::Group structuralObject_group = parent_group.get_group("structuralObject");

        omega::traverse_elements_and_add_to_vector(border_group, road.borders_, Border());
        omega::traverse_elements_and_add_to_vector(lane_group, road.lanes_, Lane());
        omega::traverse_elements_and_add_to_vector(lateralMarking_group, road.lateral_markings_, LateralMarking());
        omega::traverse_elements_and_add_to_vector(roadObject_group, road.road_objects_, RoadObject());
        omega::traverse_elements_and_add_to_vector(sign_group, road.signs_, Sign());
        omega::traverse_elements_and_add_to_vector(structuralObject_group, road.structural_objects_, StructuralObject());

        return road;
    }

// ################################################# Getter and Setter #################################################

    int Road::getRoadId() const {
        return this->road_id_;
    }

    void Road::setRoadId(int road_id) {
        this->road_id_ = road_id;
    }

    VVMRoadLocation Road::getRoadLocation() const {
        return this->road_location_;
    }

    void Road::setRoadLocation(VVMRoadLocation location) {
        this->road_location_ = location;
    }

    int Road::getNumberOfLanes() const {
        return this->lanes_->size();
    }

    const std::string &Road::getRoadName() const {
        return this->road_name_;
    }

    void Road::setRoadName(const std::string &road_name) {
        this->road_name_ = road_name;
    }

    Lanes_Ptr Road::lanes() const {
        assert(this->lanes_);
        return this->lanes_;
    }

    void Road::addLane(const Lane_Ptr &lane) {
        assert(this->lanes_);
        lane->setLaneId(static_cast<int>(this->lanes_->size()));
        this->lanes_->push_back(lane);
    }

    Borders_Ptr Road::borders() const {
        assert(this->borders_);
        return this->borders_;
    }

    void Road::addBorder(const Border_Ptr &border) {
        assert(this->borders_);
        border->setBorderId(static_cast<int>(this->borders_->size()));
        this->borders_->push_back(border);
    }

    LateralMarkings_Ptr Road::lateralMarkings() const {
        assert(this->lateral_markings_);
        return this->lateral_markings_;
    }

    void Road::addLateralMarking(const LateralMarking_Ptr &lateral_marking) {
        assert(this->lateral_markings_);
        lateral_marking->setLateralMarkingId(this->lateral_markings_->size());
        this->lateral_markings_->push_back(lateral_marking);
    }

    Signs_Ptr Road::signs() const {
        assert(this->signs_);
        return this->signs_;
    }

    void Road::addSign(const Sign_Ptr &sign) {
        assert(this->signs_);
        sign->setSignId(this->signs_->size());
        this->signs_->push_back(sign);
    }

    RoadObjects_Ptr Road::roadObjects() const {
        assert(this->road_objects_);
        return this->road_objects_;
    }

    void Road::addRoadObject(const RoadObject_Ptr &road_object) {
        assert(this->road_objects_);
        road_object->setRoadObjectId(this->road_objects_->size());
        this->road_objects_->push_back(road_object);
    }

    StructuralObjects_Ptr Road::structuralObjects() const {
        assert(this->structural_objects_);
        return this->structural_objects_;
    }

    void Road::addStructuralObject(const StructuralObject_Ptr &structural_object) {
        assert(this->structural_objects_);
        structural_object->setStructuralObjectId(this->structural_objects_->size());
        this->structural_objects_->push_back(structural_object);
    }

    std::ostream &operator<<(std::ostream &os, const Road &road) {
        os << "Id: " << road.road_id_
           << " Name: " << road.road_name_
           << " Number of lanes: " << road.lanes_->size();
        return os;
    }

}
