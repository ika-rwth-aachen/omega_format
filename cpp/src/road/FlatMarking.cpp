#include "road/FlatMarking.h"
#include "road/Lane.h"
#include "hdf5_utility.h"

namespace omega {

    FlatMarking::~FlatMarking() {
        this->flat_marking_polyline_component_x_.clear();
        this->flat_marking_polyline_component_y_.clear();
        this->flat_marking_polyline_component_z_.clear();
    }

    bool FlatMarking::to_hdf5(hdf5::node::Group &parent_group) {
        try {
            // Assert that the length of all polyline component vectors is the same
            size_t length = this->flat_marking_polyline_component_x_.size();
            assert(this->flat_marking_polyline_component_y_.size() == length);
            assert(this->flat_marking_polyline_component_z_.size() == length);
            // Writing the hdf group to a group with id as name
            hdf5::node::Group hdf5_group(parent_group.create_group(std::to_string(this->flat_marking_id_)));
            omega::add_attribute_to_group(hdf5_group, "type", static_cast<int>(this->flat_marking_type_));
            omega::add_attribute_to_group(hdf5_group, "color", static_cast<int>(this->flat_marking_color_));
            omega::add_attribute_to_group(hdf5_group, "condition", static_cast<int>(this->flat_marking_condition_));
            omega::add_attribute_to_group(hdf5_group, "value", this->flat_marking_value_);
            omega::add_dataset_to_group(hdf5_group, "overriddenBy", std::vector<int>());
            omega::add_dataset_to_group(hdf5_group, "overrides", std::vector<int>());
            omega::add_attribute_to_group(hdf5_group, "layerFlag", this->layer_flag_);
            // Polyline Subgroup
            omega::add_dataset_to_group(hdf5_group, "posX", this->flat_marking_polyline_component_x_);
            omega::add_dataset_to_group(hdf5_group, "posY", this->flat_marking_polyline_component_y_);
            omega::add_dataset_to_group(hdf5_group, "posZ", this->flat_marking_polyline_component_z_);
            // TODO Fill the empty flatmarking field "overrides"
            // TODO Fill the empty flatmarking field "overriddenBy"
            return true;
        } catch (std::exception &e) {
            std::cerr << "[ERROR] Unable to write the flatmarking to the hdf5 group: " << std::endl << e.what()
                      << std::endl;
            return false;
        }
    }

    FlatMarking FlatMarking::from_hdf5(hdf5::node::Group &parent_group) {
        FlatMarking flatMarking;
        flatMarking.flat_marking_id_ = omega::get_group_id(parent_group);

        int type, color, condition;
        omega::read_attribute(parent_group, "type", type);
        omega::read_attribute(parent_group, "color", color);
        omega::read_attribute(parent_group, "condition", condition);
        flatMarking.flat_marking_type_ = VVMFlatMarkingType(type);
        flatMarking.flat_marking_color_ = VVMFlatMarkingColor(color);
        flatMarking.flat_marking_condition_ = VVMFlatMarkingCondition(condition);

        omega::read_attribute(parent_group, "value", flatMarking.flat_marking_value_);
        omega::read_attribute(parent_group, "layerFlag", flatMarking.layer_flag_);

        //omega::read_dataset(parent_group, "overriddenBy", std::vector<int>());
        //omega::read_dataset(parent_group, "overrides", std::vector<int>());

        omega::read_dataset(parent_group, "posX", flatMarking.flat_marking_polyline_component_x_);
        omega::read_dataset(parent_group, "posY", flatMarking.flat_marking_polyline_component_y_);
        omega::read_dataset(parent_group, "posZ", flatMarking.flat_marking_polyline_component_z_);

        return flatMarking;
    }


// GETTER / SETTER
    VVMFlatMarkingColor FlatMarking::getFlatMarkingColor() const {
        return this->flat_marking_color_;
    }

    void FlatMarking::setFlatMarkingColor(VVMFlatMarkingColor flat_marking_color) {
        this->flat_marking_color_ = flat_marking_color;
    }

    int FlatMarking::getFlatMarkingId() const {
        return this->flat_marking_id_;
    }

    void FlatMarking::setFlatMarkingId(int flat_marking_id) {
        this->flat_marking_id_ = flat_marking_id;
    }

    std::weak_ptr<Lane> FlatMarking::getParent() const {
        assert(this->parent_.lock());
        return this->parent_;
    }

    void FlatMarking::setParent(const Lane_Ptr &parent) {
        this->parent_ = parent;
    }

    VVMFlatMarkingCondition FlatMarking::getFlatMarkingCondition() const {
        return this->flat_marking_condition_;
    }

    void FlatMarking::setFlatMarkingCondition(VVMFlatMarkingCondition flat_marking_condition) {
        this->flat_marking_condition_ = flat_marking_condition;
    }

    int FlatMarking::getFlatMarkingLayerFlag() const {
        return this->flat_marking_layer_flag_;
    }

    void FlatMarking::setFlatMarkingLayerFlag(int value) {
        this->flat_marking_layer_flag_ = value;
    }

    int FlatMarking::getFlatMarkingValue() const {
        return this->flat_marking_value_;
    }

    void FlatMarking::setFlatMarkingValue(int flat_marking_value) {
        this->flat_marking_value_ = flat_marking_value;
    }

    int FlatMarking::getFlatMarkingRelatedRoad() const {
        return this->flat_marking_related_road_;
    }

    void FlatMarking::setFlatMarkingRelatedRoad(int value) {
        this->flat_marking_related_road_ = value;
    }

    int FlatMarking::getFlatMarkingRelatedLane() const {
        return this->flat_marking_related_lane_;
    }

    void FlatMarking::setFlatMarkingRelatedLane(int value) {
        this->flat_marking_related_lane_ = value;
    }

    VVMFlatMarkingType FlatMarking::getFlatMarkingType() const {
        return this->flat_marking_type_;
    }

    void FlatMarking::setFlatMarkingType(VVMFlatMarkingType flat_marking_type) {
        this->flat_marking_type_ = flat_marking_type;
    }

    void FlatMarking::addFlatMarkingPolylineCompX(double value) {
        this->flat_marking_polyline_component_x_.push_back(value);
    }

    void FlatMarking::addFlatMarkingPolylineCompY(double value) {
        this->flat_marking_polyline_component_y_.push_back(value);
    }

    void FlatMarking::addFlatMarkingPolylineCompZ(double value) {
        this->flat_marking_polyline_component_z_.push_back(value);
    }

    std::ostream &operator<<(std::ostream &os, const FlatMarking &flat_marking) {
        os << "Id: " << flat_marking.flat_marking_id_
           << " Color: " << static_cast<int>(flat_marking.flat_marking_color_)
           << " Condition: " << static_cast<int>(flat_marking.flat_marking_condition_);
        return os;
    }
}
