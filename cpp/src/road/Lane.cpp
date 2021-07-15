#include "road/Lane.h"

#include "road/Surface.h"
#include "road/FlatMarking.h"
#include "road/Boundary.h"
#include "hdf5_utility.h"

namespace omega {

    Lane::Lane() {
        this->flat_markings_ = std::make_shared<FlatMarkings>();
        this->lane_boundaries_ = std::make_shared<Boundaries>();
        this->lane_surface_ = std::make_shared<Surface>();
    }

    bool Lane::to_hdf5(hdf5::node::Group &parent_group) {
        try {
            // Writing to the hdf5 file
            hdf5::node::Group hdf5_group(parent_group.create_group(std::to_string(this->lane_id_)));
            omega::add_attribute_to_group(hdf5_group, "type", static_cast<int>(this->lane_type_));
            omega::add_attribute_to_group(hdf5_group, "subtype", static_cast<int>(this->lane_sub_type_));
            omega::add_attribute_to_group(hdf5_group, "class", static_cast<int>(this->lane_class_));
            omega::add_attribute_to_group(hdf5_group, "invertedRight", this->right_border_inverted_);
            omega::add_dataset_to_group(hdf5_group, "borderRight", this->border_right_);
            omega::add_attribute_to_group(hdf5_group, "invertedLeft", this->left_lane_inverted_);
            omega::add_dataset_to_group(hdf5_group, "borderLeft", this->border_left_);
            omega::add_attribute_to_group(hdf5_group, "layerFlag", this->layer_flag_);
            omega::add_dataset_to_group(hdf5_group, "predecessor", this->predecessors_);
            omega::add_dataset_to_group(hdf5_group, "successor", this->successors_);

            // Write all boundaries to the boundary group
            hdf5::node::Group hdf5_ground_current_lane_boundary(hdf5_group.create_group("boundary"));
            for (const auto &boundary : *this->lane_boundaries_) {
                boundary->to_hdf5(hdf5_ground_current_lane_boundary);
            }

            // Write all flat markings to the Flat Marking group
            hdf5::node::Group hdf5_ground_current_lane_flatmarking(hdf5_group.create_group("flatMarking"));
            for (const auto &flatmarking : *this->flat_markings_) {
                flatmarking->to_hdf5(hdf5_ground_current_lane_flatmarking);
            }

            // Write surface
            this->lane_surface_->to_hdf5(hdf5_group);
            return true;
        } catch (std::exception &e) {
            std::cerr << "[ERROR] Unable to write the lane to the hdf5 group: " << std::endl << e.what() << std::endl;
            return false;
        }
    }

    Lane Lane::from_hdf5(hdf5::node::Group &parent_group) {
        Lane lane;
        lane.lane_id_ = omega::get_group_id(parent_group);

        int type;
        int subtype;
        int laneClass;
        omega::read_attribute(parent_group, "type", type);
        omega::read_attribute(parent_group, "subtype", subtype);
        omega::read_attribute(parent_group, "class", laneClass);
        lane.lane_type_ = VVMLaneType(type);
        lane.lane_sub_type_ = VVMLaneSubType(subtype);
        lane.lane_class_ = VVMLaneClass(laneClass);

        omega::read_attribute(parent_group, "invertedRight", lane.right_border_inverted_);
        omega::read_attribute(parent_group, "layerFlag", lane.layer_flag_);
        omega::read_attribute(parent_group, "invertedLeft", lane.left_lane_inverted_);

        std::vector<int> border_right(2);
        std::vector<int> border_left(2);
        omega::read_dataset(parent_group, "borderRight", border_right);
        omega::read_dataset(parent_group, "borderLeft", border_left);
        lane.border_right_ = std::make_pair(border_right[0], border_right[1]);
        lane.border_left_ = std::make_pair(border_left[0], border_left[1]);

        //omega::read_dataset(parent_group, "predecessor", lane.predecessors_);
        //omega::read_dataset(parent_group, "successor", lane.successors_);

        hdf5::node::Group boundary_group = parent_group.get_group("boundary");
        hdf5::node::Group flatMarking_group = parent_group.get_group("flatMarking");

        omega::traverse_elements_and_add_to_vector(boundary_group, lane.lane_boundaries_, Boundary());
        omega::traverse_elements_and_add_to_vector(flatMarking_group, lane.flat_markings_, FlatMarking());

        hdf5::node::Group surface_group = parent_group.get_group("surface");
        lane.lane_surface_ = std::make_shared<Surface>(Surface::from_hdf5(surface_group));

        return lane;
    }

// ################################################# Getter and Setter #################################################

    VVMLaneType Lane::getType() const {
        return this->lane_type_;
    }

    void Lane::setType(VVMLaneType lane_type) {
        this->lane_type_ = lane_type;
    }

    VVMLaneSubType Lane::getSubtype() const {
        return this->lane_sub_type_;
    }

    void Lane::setSubtype(VVMLaneSubType subtype) {
        this->lane_sub_type_ = subtype;
    }

    VVMLaneClass Lane::getLaneClass() const {
        return this->lane_class_;
    }

    void Lane::setLaneClass(VVMLaneClass lane_class) {
        this->lane_class_ = lane_class;
    }

    const std::set<std::pair<int, int>> &Lane::getPredecessors() const {
        return this->predecessors_;
    }

    void Lane::setPredecessors(const std::set<std::pair<int, int>> &predecessors) {
        this->predecessors_ = predecessors;
    }

    void Lane::addPredecessors(const std::pair<int, int> &predecessor) {
        this->predecessors_.insert(predecessor);
    }

    const std::set<std::pair<int, int>> &Lane::getSuccessors() const {
        return this->successors_;
    }

    void Lane::setSuccessors(const std::set<std::pair<int, int>> &successors) {
        this->successors_ = successors;
    }

    void Lane::addSuccessors(const std::pair<int, int> &successor) {
        this->successors_.insert(successor);
    }

    bool Lane::isRightBorderInverted() const {
        return this->right_border_inverted_;
    }

    void Lane::setRightBorderInverted(bool right_border_inverted) {
        this->right_border_inverted_ = right_border_inverted;
    }

    bool Lane::isLeftBorderInverted() const {
        return this->left_lane_inverted_;
    }

    void Lane::setLeftBorderInverted(bool left_border_inverted) {
        this->left_lane_inverted_ = left_border_inverted;
    }

    int Lane::getLaneId() const {
        return this->lane_id_;
    }

    void Lane::setLaneId(int lane_id) {
        this->lane_id_ = lane_id;
    }

    std::weak_ptr<Road> Lane::getParent() const {
        assert(this->parent_.lock());
        return this->parent_;
    }

    void Lane::setParent(const Road_Ptr &parent) {
        this->parent_ = parent;
    }

    const std::pair<int, int> &Lane::getBorderRight() const {
        return this->border_right_;
    }

    const std::pair<int, int> &Lane::getBorderLeft() const {
        return this->border_left_;
    }

    void Lane::setBorderRight(const std::pair<int, int> &border_right) {
        this->border_right_ = border_right;
    }

    void Lane::setBorderLeft(const std::pair<int, int> &border_left) {
        this->border_left_ = border_left;
    }

    Boundaries_Ptr Lane::laneBoundaries() const {
        return this->lane_boundaries_;
    }

    void Lane::addLaneBoundary(const Boundary_Ptr &lane_boundary) {
        assert(this->lane_boundaries_);
        lane_boundary->setBoundaryId(this->lane_boundaries_->size());
        this->lane_boundaries_->push_back(lane_boundary);
    }

    FlatMarkings_Ptr Lane::flatMarkings() const {
        return this->flat_markings_;
    }

    void Lane::addFlatMarking(const FlatMarking_Ptr &lane_flatMarking) {
        assert(this->flat_markings_);
        lane_flatMarking->setFlatMarkingId(this->flat_markings_->size());
        this->flat_markings_->push_back(lane_flatMarking);
    }

    int Lane::getLayerFlag() const {
        return this->layer_flag_;
    }

    void Lane::setLayerFlag(int layer_flag) {
        this->layer_flag_ = layer_flag;
    }

    Surface_Ptr Lane::laneSurface() const {
        return lane_surface_;
    }

    std::ostream &operator<<(std::ostream &os, const Lane &lane) {
        os << "Id: " << lane.lane_id_
           << " Type: " << static_cast<int>(lane.lane_type_)
           << " Sub Type: " << static_cast<int>(lane.lane_sub_type_)
           << " Class: " << static_cast<int>(lane.lane_class_);
        return os;
    }
}
