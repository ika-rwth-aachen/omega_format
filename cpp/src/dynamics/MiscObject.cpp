#include "dynamics/MiscObject.h"
#include "hdf5_utility.h"

namespace omega {

    MiscObject::MiscObject() : tr(0) {
        this->birthStamp = 0;
        this->id = "M0";
        type_ = VVMMiscObjectType::UNKNOWN;
        subtype_ = VVMMiscObjectSubType::UNKNOWN;
    }

    bool MiscObject::to_hdf5(hdf5::node::Group &parent_group) {
        hdf5::node::Group ru_group(parent_group.create_group(this->id));

        bb.to_hdf5(ru_group);
        tr.to_hdf5(ru_group);

        int type = static_cast<int>(this->type_);
        int subtype = static_cast<int>(this->subtype_);
        omega::add_attribute_to_group(ru_group, "type", type);
        omega::add_attribute_to_group(ru_group, "subtype", subtype);
        omega::add_attribute_to_group(ru_group, "connectedTo", this->connectedTo);
        omega::add_attribute_to_group(ru_group, "attachedTo", this->attachedTo);
        return true;
    }

    MiscObject MiscObject::from_hdf5(hdf5::node::Group &parent_group) {
        MiscObject miscObject;

        int type, subtype;
        omega::read_attribute(parent_group, "type", type);
        omega::read_attribute(parent_group, "subtype", subtype);
        miscObject.type_ = VVMMiscObjectType(type);
        miscObject.subtype_ = VVMMiscObjectSubType(subtype);

        miscObject.id = omega::get_group_id(parent_group);
        omega::read_attribute(parent_group, "birthStamp", miscObject.birthStamp);
        omega::read_attribute(parent_group, "connectedTo", miscObject.connectedTo);
        omega::read_attribute(parent_group, "attachedTo", miscObject.attachedTo);
        hdf5::node::Group bound_box_group = parent_group.get_group("boundBox");
        hdf5::node::Group trajectory_group = parent_group.get_group("trajectory");
        hdf5::node::Group vehicle_lights_group = parent_group.get_group("vehicleLights");
        miscObject.bb = BoundingBox::from_hdf5(bound_box_group);
        miscObject.tr = Trajectory::from_hdf5(trajectory_group);

        return miscObject;
    }
}
