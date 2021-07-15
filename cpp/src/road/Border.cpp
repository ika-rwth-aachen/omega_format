#include "road/Border.h"
#include "hdf5_utility.h"
#include "road/Road.h"
#include <cmath>

namespace omega {

    bool Border::to_hdf5(hdf5::node::Group &parent_group) {
        try {
            // Assert that the length of all polyline component vectors is the same
            size_t length = this->border_polyline_component_x_.size();
            assert(this->border_polyline_component_y_.size() == length);
            assert(this->border_polyline_component_z_.size() == length);

            // Writing the hdf group id as name
            hdf5::node::Group hdf5_group(parent_group.create_group(std::to_string(this->border_id_)));
            omega::add_dataset_to_group(hdf5_group, "posX", this->border_polyline_component_x_);
            omega::add_dataset_to_group(hdf5_group, "posY", this->border_polyline_component_y_);
            omega::add_dataset_to_group(hdf5_group, "posZ", this->border_polyline_component_z_);
            return true;

        } catch (std::exception &e) {
            std::cerr << "[ERROR] Unable to write the border to the hdf5 group: " << std::endl << e.what() << std::endl;
            return false;
        }
    }

    Border Border::from_hdf5(hdf5::node::Group &parent_group) {
        Border border;

        border.border_id_ = omega::get_group_id(parent_group);
        omega::read_dataset(parent_group, "posX", border.border_polyline_component_x_);
        omega::read_dataset(parent_group, "posY", border.border_polyline_component_y_);
        omega::read_dataset(parent_group, "posZ", border.border_polyline_component_z_);

        return border;
    }

// ################################################# Getter and Setter #################################################

    void Border::addToBorderPolyline(const double x, const double y, const double z) {
        this->border_polyline_component_x_.push_back(x);
        this->border_polyline_component_y_.push_back(y);
        this->border_polyline_component_z_.push_back(z);
    }

    int Border::getBorderId() const {
        return this->border_id_;
    }

    void Border::setBorderId(int border_id) {
        this->border_id_ = border_id;
    }

    std::weak_ptr<Road> Border::getParent() const {
        assert(this->parent_.lock());
        return this->parent_;
    }

    void Border::setParent(const Road_Ptr &parent) {
        this->parent_ = parent;
    }

    size_t Border::getBorderPolylineIndex() {
        return std::max(static_cast<int>(this->border_polyline_component_x_.size() - 1), 0);
    }

    std::vector<double> Border::getBorderPolylineCompX() {
        return this->border_polyline_component_x_;
    }

    std::vector<double> Border::getBorderPolylineCompY() {
        return this->border_polyline_component_y_;
    }

    std::vector<double> Border::getBorderPolylineCompZ() {
        return this->border_polyline_component_z_;
    }

    std::ostream &operator<<(std::ostream &os, const Border &border) {
        os << "Id: " << border.border_id_;
        return os;
    }

    bool Border::operator==(Border &border) {
        auto x = border.getBorderPolylineCompX();
        if (x.size() != this->border_polyline_component_x_.size()) {
            return false;
        }
        auto y = border.getBorderPolylineCompY();
        if (y.size() != this->border_polyline_component_y_.size()) {
            return false;
        }
        auto z = border.getBorderPolylineCompZ();
        if (z.size() != this->border_polyline_component_z_.size()) {
            return false;
        }
        for (size_t i = 0; i < x.size(); i++) {
            if (x[i] != this->border_polyline_component_x_[i]) {
                return false;
            }
        }
        for (size_t i = 0; i < y.size(); i++) {
            if (y[i] != this->border_polyline_component_y_[i]) {
                return false;
            }
        }
        for (size_t i = 0; i < z.size(); i++) {
            if (z[i] != this->border_polyline_component_z_[i]) {
                return false;
            }
        }

        return true;
    }
}
