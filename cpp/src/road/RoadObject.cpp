#include "road/RoadObject.h"
#include "hdf5_utility.h"

namespace omega {

    bool RoadObject::to_hdf5(hdf5::node::Group &parent_group) const {
        try {
            // Writing the hdf group to a group with id as name
            hdf5::node::Group hdf5_group(parent_group.create_group(std::to_string(this->road_object_id_)));
            omega::add_attribute_to_group(hdf5_group, "type", static_cast<int>(this->road_object_type_));
            omega::add_attribute_to_group(hdf5_group, "height", this->road_object_height_);
            omega::add_attribute_to_group(hdf5_group, "drivable", this->driveable_);
            omega::add_attribute_to_group(hdf5_group, "walkable", this->walkable_);

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

    RoadObject RoadObject::from_hdf5(hdf5::node::Group &parent_group) {
        RoadObject roadObject;
        roadObject.road_object_id_ = omega::get_group_id(parent_group);

        int type;
        omega::read_attribute(parent_group, "type", type);
        roadObject.road_object_type_ = VVMRoadObjectType(type);
        omega::read_attribute(parent_group, "height", roadObject.road_object_height_);
        omega::read_attribute(parent_group, "drivable", roadObject.driveable_);
        omega::read_attribute(parent_group, "walkable", roadObject.walkable_);
        omega::read_attribute(parent_group, "layerFlag", roadObject.layer_flag_);

        omega::read_dataset(parent_group, "posX", roadObject.polyline_component_x_);
        omega::read_dataset(parent_group, "posY", roadObject.polyline_component_y_);
        omega::read_dataset(parent_group, "posZ", roadObject.polyline_component_z_);

        //omega::read_dataset(parent_group, "overriddenBy", std::vector<int>());
        //omega::read_dataset(parent_group, "overrides", std::vector<int>());

        return roadObject;
    }

    int RoadObject::getRoadObjectId() const {
        return road_object_id_;
    }

    void RoadObject::setRoadObjectId(int road_object_id) {
        road_object_id_ = road_object_id;
    }

    std::weak_ptr<Road> RoadObject::getParent() const {
        assert(this->parent_.lock());
        return this->parent_;
    }

    void RoadObject::setParent(const Road_Ptr &parent) {
        this->parent_ = parent;
    }

    VVMRoadObjectType RoadObject::getRoadObjectType() const {
        return road_object_type_;
    }

    void RoadObject::setRoadObjectType(VVMRoadObjectType road_object_type) {
        road_object_type_ = road_object_type;
    }

    bool RoadObject::isWalkable() const {
        return walkable_;
    }

    void RoadObject::setWalkable(bool walkable) {
        walkable_ = walkable;
    }

    bool RoadObject::isDriveable() const {
        return driveable_;
    }

    void RoadObject::setDriveable(bool driveable) {
        driveable_ = driveable;
    }

    double RoadObject::getRoadObjectHeight() const {
        return road_object_height_;
    }

    void RoadObject::setRoadObjectHeight(double road_object_height) {
        road_object_height_ = road_object_height;
    }

    int RoadObject::getLayerFlag() const {
        return layer_flag_;
    }

    void RoadObject::setLayerFlag(int layer_flag) {
        layer_flag_ = layer_flag;
    }

    void RoadObject::addToRoadObjectPolyline(const double x, const double y, const double z) {
        this->polyline_component_x_.push_back(x);
        this->polyline_component_y_.push_back(y);
        this->polyline_component_z_.push_back(z);
    }

    std::ostream &operator<<(std::ostream &os, const RoadObject &object) {
        os << "Id: " << object.road_object_id_
           << " Type: " << static_cast<int>(object.road_object_type_)
           << " Walkable: " << (object.walkable_ ? "true" : "false")
           << " Driveable: " << (object.driveable_ ? "true" : "false")
           << " Height: " << object.road_object_height_;
        return os;
    }

}
