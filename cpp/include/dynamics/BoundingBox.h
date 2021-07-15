#ifndef BOUNDINGBOX_H
#define BOUNDINGBOX_H

#include <h5cpp/hdf5.hpp>

class BoundingBox {
    double length;
    double width;
    double height;

    int confidentLength;
    int confidentWidth;

public:
    BoundingBox();

    double getLength() const;

    void setLength(double value);

    double getWidth() const;

    void setWidth(double value);

    double getHeight() const;

    void setHeight(double value);

    // hdf5
    void to_hdf5(hdf5::node::Group &parent_group);
    static BoundingBox from_hdf5(hdf5::node::Group &parent_group);
};


#endif // BOUNDINGBOX_H
