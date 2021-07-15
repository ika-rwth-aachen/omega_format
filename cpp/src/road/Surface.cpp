#include "road/Surface.h"
#include "hdf5_utility.h"

namespace omega {

    bool Surface::to_hdf5(hdf5::node::Group &parent_group) {
        try {
            // Writing the hdf group to a group with id as name
            hdf5::node::Group hdf5_ground(parent_group.create_group("surface"));
            omega::add_attribute_to_group(hdf5_ground, "material", static_cast<int>(this->surface_material_));
            omega::add_attribute_to_group(hdf5_ground, "color", static_cast<int>(this->surface_color_));
            omega::add_attribute_to_group(hdf5_ground, "condition", static_cast<int>(this->surface_condition_));
            omega::add_attribute_to_group(hdf5_ground, "layerFlag", this->layer_flag_);
            omega::add_dataset_to_group(hdf5_ground, "overriddenBy", std::vector<int>());
            omega::add_dataset_to_group(hdf5_ground, "overrides", std::vector<int>());

            // TODO Fill the empty boundary field "overrides"
            // TODO Fill the empty boundary field "overriddenBy"
            return true;
        } catch (std::exception &e) {

            return false;
        }
    }

// ################################################# Getter and Setter #################################################

    std::weak_ptr<Lane> Surface::getParent() const {
        assert(this->parent_.lock());
        return this->parent_;
    }

    void Surface::setParent(const Lane_Ptr &parent) {
        this->parent_ = parent;
    }

    VVMSurfaceMaterial Surface::getSurfaceMaterial() const {
        return this->surface_material_;
    }

    void Surface::setSurfaceMaterial(VVMSurfaceMaterial surface_material) {
        this->surface_material_ = surface_material;
    }

    VVMSurfaceColor Surface::getSurfaceColor() const {
        return this->surface_color_;
    }

    void Surface::setSurfaceColor(VVMSurfaceColor surface_color) {
        this->surface_color_ = surface_color;
    }

    VVMSurfaceCondition Surface::getSurfaceCondition() const {
        return this->surface_condition_;
    }

    void Surface::setSurfaceCondition(VVMSurfaceCondition surface_condition) {
        this->surface_condition_ = surface_condition;
    }

    int Surface::getLayerFlag() const {
        return this->layer_flag_;
    }

    void Surface::setLayerFlag(int layer_flag) {
        this->layer_flag_ = layer_flag;
    }

    std::ostream &operator<<(std::ostream &os, const Surface &surface) {
        os << "Material: " << static_cast<int>(surface.surface_material_)
           << " Color: " << static_cast<int>(surface.surface_color_)
           << " Condition: " << static_cast<int>(surface.surface_condition_);
        return os;
    }

    Surface Surface::from_hdf5(hdf5::node::Group &parent_group) {
        Surface surface;

        return surface;
    }

}
