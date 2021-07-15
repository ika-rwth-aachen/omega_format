#include "road/Boundary.h"
#include "hdf5_utility.h"

#include "road/Lane.h"
#include "road/Border.h"

namespace omega {


    bool Boundary::to_hdf5(hdf5::node::Group &parent_group) {
        try {
            // Assert a correct index order
            assert(this->poly_index_start_ <= this->poly_index_end_);

            // Writing the hdf group to a group with id as name
            hdf5::node::Group hdf5_group(parent_group.create_group(std::to_string(this->boundary_id_)));
            omega::add_attribute_to_group(hdf5_group, "type", static_cast<int>(this->boundary_type_));
            omega::add_attribute_to_group(hdf5_group, "subtype", static_cast<int>(this->boundary_sub_type_));
            omega::add_attribute_to_group(hdf5_group, "right", this->boundary_is_on_right_side_);
            omega::add_attribute_to_group(hdf5_group, "height", this->boundary_height_);
            omega::add_attribute_to_group(hdf5_group, "color", static_cast<int>(this->boundary_color_));
            omega::add_attribute_to_group(hdf5_group, "condition", static_cast<int>(this->boundary_condition_));
            omega::add_attribute_to_group(hdf5_group, "polyIndexStart", this->poly_index_start_);
            omega::add_attribute_to_group(hdf5_group, "polyIndexEnd", this->poly_index_end_);
            omega::add_attribute_to_group(hdf5_group, "layerFlag", this->layer_flag_);
            omega::add_dataset_to_group(hdf5_group, "overriddenBy", std::vector<int>());
            omega::add_dataset_to_group(hdf5_group, "overrides", std::vector<int>());

            // TODO Fill the empty boundary field "overrides"
            // TODO Fill the empty boundary field "overriddenBy"
            return true;
        } catch (std::exception &e) {
            std::cerr << "[ERROR] Unable to write the boundary to the hdf5 group: " << std::endl << e.what()
                      << std::endl;
            return false;
        }
    }

    Boundary Boundary::from_hdf5(hdf5::node::Group &parent_group) {
        Boundary boundary;

        boundary.boundary_id_ = omega::get_group_id(parent_group);

        int type, subtype, color, condition;
        omega::read_attribute(parent_group, "type", type);
        omega::read_attribute(parent_group, "subtype", subtype);
        omega::read_attribute(parent_group, "color", color);
        omega::read_attribute(parent_group, "condition", condition);
        boundary.boundary_type_ = VVMBoundaryType(type);
        boundary.boundary_sub_type_ = VVMBoundarySubType(subtype);
        boundary.boundary_color_ = VVMBoundaryColor(color);
        boundary.boundary_condition_ = VVMBoundaryCondition(condition);

        omega::read_attribute(parent_group, "right", boundary.boundary_is_on_right_side_);
        omega::read_attribute(parent_group, "height", boundary.boundary_height_);
        omega::read_attribute(parent_group, "polyIndexStart", boundary.poly_index_start_);
        omega::read_attribute(parent_group, "polyIndexEnd", boundary.poly_index_end_);
        omega::read_attribute(parent_group, "layerFlag", boundary.layer_flag_);

        //omega::read_dataset(parent_group, "overriddenBy", std::vector<int>());
        //omega::read_dataset(parent_group, "overrides", std::vector<int>());

        return boundary;
    }

// ################################################# Getter and Setter #################################################
    int Boundary::getBoundaryId() const {
        return boundary_id_;
    }

    void Boundary::setBoundaryId(int boundary_id) {
        boundary_id_ = boundary_id;
    }

    std::weak_ptr<Lane> Boundary::getParent() const {
        assert(this->parent_.lock());
        return this->parent_;
    }

    void Boundary::setParent(const Lane_Ptr &parent) {
        this->parent_ = parent;
    }

    VVMBoundaryType Boundary::getBoundaryType() const {
        return boundary_type_;
    }

    void Boundary::setBoundaryType(VVMBoundaryType boundary_type) {
        boundary_type_ = boundary_type;
    }

    VVMBoundarySubType Boundary::getBoundarySubType() const {
        return boundary_sub_type_;
    }

    void Boundary::setBoundarySubType(VVMBoundarySubType boundary_sub_type) {
        boundary_sub_type_ = boundary_sub_type;
    }

    VVMBoundaryColor Boundary::getBoundaryColor() const {
        return boundary_color_;
    }

    void Boundary::setBoundaryColor(VVMBoundaryColor boundary_color) {
        boundary_color_ = boundary_color;
    }

    VVMBoundaryCondition Boundary::getBoundaryCondition() const {
        return boundary_condition_;
    }

    void Boundary::setBoundaryCondition(VVMBoundaryCondition boundary_condition) {
        boundary_condition_ = boundary_condition;
    }

    bool Boundary::isBoundaryIsOnRightSide() const {
        return boundary_is_on_right_side_;
    }

    void Boundary::setBoundaryIsOnRightSide(bool boundary_is_on_right_side) {
        boundary_is_on_right_side_ = boundary_is_on_right_side;
    }

    double Boundary::getBoundaryHeight() const {
        return boundary_height_;
    }

    void Boundary::setBoundaryHeight(double boundary_height) {
        Boundary::boundary_height_ = boundary_height;
    }

    int Boundary::getLayerFlag() const {
        return layer_flag_;
    }

    void Boundary::setLayerFlag(int layer_flag) {
        layer_flag_ = layer_flag;
    }

    int Boundary::getPolyIndexStart() const {
        return poly_index_start_;
    }

    void Boundary::setPolyIndexStart(int poly_index_start) {
        poly_index_start_ = poly_index_start;
    }

    int Boundary::getPolyIndexEnd() const {
        return poly_index_end_;
    }

    void Boundary::setPolyIndexEnd(int poly_index_end) {
        poly_index_end_ = poly_index_end;
    }

    std::ostream &operator<<(std::ostream &os, const Boundary &boundary) {
        os << "Id: " << boundary.boundary_id_
           << " Type: " << static_cast<int>(boundary.boundary_type_)
           << " Sub Type: " << static_cast<int>(boundary.boundary_sub_type_)
           << " Right Side: " << (boundary.boundary_is_on_right_side_ ? "true" : "false");
        return os;
    }

}
