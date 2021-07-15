#include <dynamics/BoundingBox.h>
#include "hdf5_utility.h"

BoundingBox::BoundingBox() {
    this->length = 0.0;
    this->width = 0.0;
    this->height = 0.0;

    this->confidentLength = true; // true for inD drone data
    this->confidentWidth = true; // true for inD drone data
}

double BoundingBox::getLength() const {
    return length;
}

void BoundingBox::setLength(double value) {
    length = value;
}

double BoundingBox::getWidth() const {
    return width;
}

void BoundingBox::setWidth(double value) {
    width = value;
}

double BoundingBox::getHeight() const {
    return height;
}

void BoundingBox::setHeight(double value) {
    height = value;
}

void BoundingBox::to_hdf5(hdf5::node::Group &parent_group) {
    // Writing the hdf group to a group with id as name
    hdf5::node::Group boundbox_group(parent_group.create_group("boundBox"));

    hdf5::node::Dataset dset_length = omega::add_dataset_to_group(boundbox_group, "length", this->length);
    hdf5::node::Dataset dset_width = omega::add_dataset_to_group(boundbox_group, "width", this->width);
    hdf5::node::Dataset dset_height = omega::add_dataset_to_group(boundbox_group, "height", this->height);

    omega::add_attribute_to_dataset(dset_length, "confident", this->confidentLength);
    omega::add_attribute_to_dataset(dset_width, "confident", this->confidentWidth);
}

BoundingBox BoundingBox::from_hdf5(hdf5::node::Group &parent_group) {
    BoundingBox boundingBox;

    //omega::read_attribute(parent_group, "confident", boundingBox.confidentLength);
    //omega::read_attribute(parent_group, "confident", boundingBox.confidentWidth);

    omega::read_scalar_dataset(parent_group, "length", boundingBox.length);
    omega::read_scalar_dataset(parent_group, "width", boundingBox.width);
    omega::read_scalar_dataset(parent_group, "height", boundingBox.height);

    return boundingBox;
}
