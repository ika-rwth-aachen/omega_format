#include "road/LateralMarking.h"
#include "road/Road.h"
#include "hdf5_utility.h"

namespace omega {

    bool LateralMarking::to_hdf5(hdf5::node::Group &parent_group) {
        try {
            // Assert that the length of all polyline component vectors is the same
            size_t length = this->lateral_marking_polyline_component_x_.size();
            assert(this->lateral_marking_polyline_component_y_.size() == length);
            assert(this->lateral_marking_polyline_component_z_.size() == length);

            // Writing the hdf group to a group with id as name
            hdf5::node::Group hdf5_group(parent_group.create_group(std::to_string(this->lateral_marking_id_)));
            omega::add_attribute_to_group(hdf5_group, "type", static_cast<int>(this->lateral_marking_type_));
            omega::add_attribute_to_group(hdf5_group, "longSize", this->lateral_marking_long_size_);
            omega::add_attribute_to_group(hdf5_group, "color", static_cast<int>(this->lateral_marking_color_));
            omega::add_attribute_to_group(hdf5_group, "condition", static_cast<int>(this->lateral_marking_condition_));
            omega::add_attribute_to_group(hdf5_group, "layerFlag", this->layer_flag_);
            omega::add_dataset_to_group(hdf5_group, "overriddenBy", std::vector<int>());
            omega::add_dataset_to_group(hdf5_group, "overrides", std::vector<int>());
            omega::add_dataset_to_group(hdf5_group, "applicableLanes", this->lateral_marking_lane_ids_);
            // Write polyline node
            omega::add_dataset_to_group(hdf5_group, "posX", this->lateral_marking_polyline_component_x_);
            omega::add_dataset_to_group(hdf5_group, "posY", this->lateral_marking_polyline_component_y_);
            omega::add_dataset_to_group(hdf5_group, "posZ", this->lateral_marking_polyline_component_z_);

            // TODO Fill the empty boundary field "overrides"
            // TODO Fill the empty boundary field "overriddenBy"
            return true;
        } catch (std::exception &e) {

            return false;
        }
    }

    LateralMarking LateralMarking::from_hdf5(hdf5::node::Group &parent_group) {
        LateralMarking lateralMarking;
        lateralMarking.lateral_marking_id_ = omega::get_group_id(parent_group);

        int type, color, condition;
        omega::read_attribute(parent_group, "type", type);
        omega::read_attribute(parent_group, "color", color);
        omega::read_attribute(parent_group, "condition", condition);
        lateralMarking.lateral_marking_type_ = VVMLateralMarkingType(type);
        lateralMarking.lateral_marking_color_ = VVMLateralMarkingColor(color);
        lateralMarking.lateral_marking_condition_ = VVMLateralMarkingCondition(condition);

        omega::read_attribute(parent_group, "longSize", lateralMarking.lateral_marking_long_size_);
        omega::read_attribute(parent_group, "layerFlag", lateralMarking.layer_flag_);

        //omega::add_dataset_to_group(parent_group, "overriddenBy", std::vector<int>());
        //omega::add_dataset_to_group(parent_group, "overrides", std::vector<int>());
        //omega::read_dataset(parent_group, "applicableLanes", lateralMarking.lateral_marking_lane_ids_);

        omega::read_dataset(parent_group, "posX", lateralMarking.lateral_marking_polyline_component_x_);
        omega::read_dataset(parent_group, "posY", lateralMarking.lateral_marking_polyline_component_y_);
        omega::read_dataset(parent_group, "posZ", lateralMarking.lateral_marking_polyline_component_z_);

        return lateralMarking;
    }

// ################################################# Getter and Setter #################################################

    void LateralMarking::addToLateralMarkingPolyline(const double x, const double y, const double z) {
        this->lateral_marking_polyline_component_x_.push_back(x);
        this->lateral_marking_polyline_component_y_.push_back(y);
        this->lateral_marking_polyline_component_z_.push_back(z);
    }

    int LateralMarking::getLateralMarkingId() const {
        return this->lateral_marking_id_;
    }

    void LateralMarking::setLateralMarkingId(int lateral_marking_id) {
        this->lateral_marking_id_ = lateral_marking_id;
    }

    std::weak_ptr<Road> LateralMarking::getParent() const {
        assert(this->parent_.lock());
        return this->parent_;
    }

    void LateralMarking::setParent(const Road_Ptr &parent) {
        this->parent_ = parent;
    }

    VVMLateralMarkingType LateralMarking::getLateralMarkingType() const {
        return this->lateral_marking_type_;
    }

    void LateralMarking::setLateralMarkingType(VVMLateralMarkingType lateral_marking_type) {
        this->lateral_marking_type_ = lateral_marking_type;
    }

    VVMLateralMarkingColor LateralMarking::getLateralMarkingColor() const {
        return this->lateral_marking_color_;
    }

    void LateralMarking::setLateralMarkingColor(VVMLateralMarkingColor lateral_marking_color) {
        this->lateral_marking_color_ = lateral_marking_color;
    }

    VVMLateralMarkingCondition LateralMarking::getLateralMarkingCondition() const {
        return this->lateral_marking_condition_;
    }

    void LateralMarking::setLateralMarkingCondition(VVMLateralMarkingCondition lateral_marking_condition) {
        this->lateral_marking_condition_ = lateral_marking_condition;
    }

    double LateralMarking::getLateralMarkingLongSize() const {
        return this->lateral_marking_long_size_;
    }

    void LateralMarking::setLateralMarkingLongSize(double lateral_marking_long_size) {
        this->lateral_marking_long_size_ = lateral_marking_long_size;
    }

    int LateralMarking::getLayerFlag() const {
        return this->layer_flag_;
    }

    void LateralMarking::setLayerFlag(int layer_flag) {
        this->layer_flag_ = layer_flag;
    }

    const std::set<std::pair<int, int>> &LateralMarking::getLanes() const {
        return this->lateral_marking_lane_ids_;
    }

    void LateralMarking::setLanes(const std::set<std::pair<int, int>> &road_lane_id_tuples) {
        this->lateral_marking_lane_ids_ = road_lane_id_tuples;
    }

    void LateralMarking::addLane(const std::pair<int, int> &road_lane_id_tuple) {
        this->lateral_marking_lane_ids_.insert(road_lane_id_tuple);
    }

    std::ostream &operator<<(std::ostream &os, const LateralMarking &marking) {
        os << "Id: " << marking.lateral_marking_id_
           << " Type: " << static_cast<int>(marking.lateral_marking_type_)
           << " Color: " << static_cast<int>(marking.lateral_marking_color_)
           << " Condition: " << static_cast<int>(marking.lateral_marking_condition_)
           << " Number of Lanes: " << marking.lateral_marking_lane_ids_.size();
        return os;
    }
}
