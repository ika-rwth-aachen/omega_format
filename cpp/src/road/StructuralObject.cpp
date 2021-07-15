#include "road/StructuralObject.h"
#include "road/Road.h"
#include "hdf5_utility.h"

namespace omega {

    bool StructuralObject::to_hdf5(hdf5::node::Group &parent_group) const {
        try {
            // Writing the hdf group to a group with id as name
            hdf5::node::Group
                    hdf5_group(parent_group.create_group(std::to_string(this->structural_object_id_)));
            omega::add_attribute_to_group(hdf5_group, "type", static_cast<int>(this->structural_object_type_));
            omega::add_attribute_to_group(hdf5_group, "height", this->structural_object_height_);

            // Write polyline node
            omega::add_dataset_to_group(hdf5_group, "posX", this->polyline_component_x_);
            omega::add_dataset_to_group(hdf5_group, "posY", this->polyline_component_y_);
            omega::add_dataset_to_group(hdf5_group, "posZ", this->polyline_component_z_);

            omega::add_dataset_to_group(hdf5_group, "overriddenBy", std::vector<int>());
            omega::add_dataset_to_group(hdf5_group, "overrides", std::vector<int>());
            omega::add_attribute_to_group(hdf5_group, "layerFlag", this->layer_flag_);

            // TODO Fill the empty boundary field "overrides"
            // TODO Fill the empty boundary field "overriddenBy"
            return true;
        } catch (std::exception &e) {

            return false;
        }
    }

    StructuralObject StructuralObject::from_hdf5(hdf5::node::Group &parent_group) {
        StructuralObject structuralObject;
        structuralObject.structural_object_id_ = omega::get_group_id(parent_group);

        int type;
        omega::read_attribute(parent_group, "type", type);
        structuralObject.structural_object_type_ = VVMStructuralObjectType(type);
        omega::read_attribute(parent_group, "height",structuralObject.structural_object_height_);
        omega::read_attribute(parent_group, "layerFlag",structuralObject.layer_flag_);

        omega::read_dataset(parent_group, "posX",structuralObject.polyline_component_x_);
        omega::read_dataset(parent_group, "posY",structuralObject.polyline_component_y_);
        omega::read_dataset(parent_group, "posZ",structuralObject.polyline_component_z_);

        //omega::read_dataset(parent_group, "overriddenBy", std::vector<int>());
        //omega::read_dataset(parent_group, "overrides", std::vector<int>());

        return structuralObject;
    }

    int StructuralObject::getStructuralObjectId() const {
        return structural_object_id_;
    }

    void StructuralObject::setStructuralObjectId(int structural_object_id) {
        structural_object_id_ = structural_object_id;
    }

    std::weak_ptr<Road> StructuralObject::getParent() const {
        assert(this->parent_.lock());
        return this->parent_;
    }

    void StructuralObject::setParent(const Road_Ptr &parent) {
        this->parent_ = parent;
    }

    VVMStructuralObjectType StructuralObject::getStructuralObjectType() const {
        return structural_object_type_;
    }

    void StructuralObject::setStructuralObjectType(VVMStructuralObjectType structural_object_type) {
        structural_object_type_ = structural_object_type;
    }

    double StructuralObject::getStructuralObjectHeight() const {
        return structural_object_height_;
    }

    void StructuralObject::setStructuralObjectHeight(double structural_object_height) {
        structural_object_height_ = structural_object_height;
    }

    int StructuralObject::getLayerFlag() const {
        return layer_flag_;
    }

    void StructuralObject::setLayerFlag(int layer_flag) {
        layer_flag_ = layer_flag;
    }

    void StructuralObject::addToStructuralObjectPolyline(const double x, const double y, const double z) {
        this->polyline_component_x_.push_back(x);
        this->polyline_component_y_.push_back(y);
        this->polyline_component_z_.push_back(z);
    }

    std::ostream &operator<<(std::ostream &os, const StructuralObject &object) {
        os << "Id: " << object.structural_object_id_
           << " Type: " << static_cast<int>(object.structural_object_type_)
           << " Height: " << object.structural_object_height_;
        return os;
    }

}
