/**
 * @file Lane.h
 * @authors Simon Schaefer
 * @date 23.09.2020
 */

#ifndef OMEGA_LANE_H
#define OMEGA_LANE_H

#include <set>
#include <ostream>
#include <vector>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

// Class forward declarations to prevent include loops
    class Boundary;

    class Road;

    class Surface;

    class FlatMarking;

    typedef std::shared_ptr<Road> Road_Ptr;
    typedef std::shared_ptr<Boundary> Boundary_Ptr;
    typedef std::vector<Boundary_Ptr> Boundaries;
    typedef std::shared_ptr<Boundaries> Boundaries_Ptr;
    typedef std::shared_ptr<Surface> Surface_Ptr;
    typedef std::shared_ptr<FlatMarking> FlatMarking_Ptr;
    typedef std::vector<FlatMarking_Ptr> FlatMarkings;
    typedef std::shared_ptr<FlatMarkings> FlatMarkings_Ptr;

/**
 * Class representing a lane defined by the VVM definitions.
 */
    class Lane {

        int lane_id_{}; ///< Unique id of this lane. This id should be unique inside a road.
        std::weak_ptr<Road> parent_; ///< Reference to parent

        VVMLaneType lane_type_ = VVMLaneType::TODO; ///< Type of lane. (street, walkway etc.)
        VVMLaneSubType lane_sub_type_ = VVMLaneSubType::TODO; ///< Subtype of lane. (bridge, tunnel etc.)
        VVMLaneClass lane_class_ = VVMLaneClass::NONE; ///< Lane class. (intersection, roundabout etc.)

        bool right_border_inverted_{}; ///< Flag that indicates that the right border is in inverted order.
        std::pair<int, int> border_right_; ///< Right border as a pointer to the road id and border id.
        bool left_lane_inverted_{}; ///< Flag that indicates that the left border is in inverted order.
        std::pair<int, int> border_left_; ///< Left border as a pointer to the road id and border id.

        // The set prevents duplicates without checking them in the code.
        std::set<std::pair<int, int>> predecessors_; ///< List of pointers to the precessing road id and lane id.
        std::set<std::pair<int, int>> successors_; ///< List of pointers to the successive road id and lane id.

        Boundaries_Ptr lane_boundaries_; ///< All boundaries that are outlying the lane.
        FlatMarkings_Ptr flat_markings_; ///< All flat markings that are on the lane.

        Surface_Ptr lane_surface_; ///< Lane surface

        int layer_flag_ = 0;  ///< Indicates if the changes are temporary or not. 0/1/2 = Permanent, 3 = Non-Permanent

    public:

        /**
         * The constructor initialises the shard pointers of which the lane is parent by design.
         */
        Lane();

        /**
         * Write to the hdf5 file. This function will create a subgroup with the lane_id as name. This function does not
         * perform a check id the subgroup may already exist.
         * @param parent_group Group there the subgroup should be added to.
         */
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Lane from_hdf5(hdf5::node::Group &parent_group);

        /**
         * Getter for the lane id. This should be unique inside a road.
         * @return Unique lane id.
         */
        [[nodiscard]] int getLaneId() const;

        /**
         * Setter for the lane id. This should be unique inside a road. Make sure this yourself there are no checks.
         * @param lane_id Unique lane id.
         */
        void setLaneId(int lane_id);

        [[nodiscard]] std::weak_ptr<Road> getParent() const;

        void setParent(const Road_Ptr &parent);

        /**
         * Getter for the inverted flag og the right border. Indication that the polyline is in reverse order.
         * @return True of the right border is inverted.
         */
        [[nodiscard]] bool isRightBorderInverted() const;

        /**
         * Setter for the inverted flag of the right border.
         * @param right_border_inverted True if the right border is inverted.
         */
        void setRightBorderInverted(bool right_border_inverted);

        /**
         * Getter for the inverted flag og the left border. Indication that the polyline is in reverse order.
         * @return True of the left border is inverted.
         */
        [[nodiscard]] bool isLeftBorderInverted() const;

        /**
         * Setter for the inverted flag of the left border.
         * @param left_border_inverted True if the left border is inverted.
         */
        void setLeftBorderInverted(bool left_border_inverted);

        /**
         * Getter for the lane type.
         * @return Current lane type.
         */
        [[nodiscard]] VVMLaneType getType() const;

        /**
         * Setter for the lane type.
         * @param lane_type New lane type.
         */
        void setType(VVMLaneType lane_type);

        /**
         * Getter for the lane sub type.
         * @return Current lane sub type.
         */
        [[nodiscard]] VVMLaneSubType getSubtype() const;

        /**
         * Setter for the lane sub type.
         * @param lane_type New lane sub type.
         */
        void setSubtype(VVMLaneSubType subtype);

        /**
         * Getter for the lane class.
         * @return Current lane class.
         */
        [[nodiscard]] VVMLaneClass getLaneClass() const;

        /**
         * Setter for the lane class.
         * @param lane_type New lane class.
         */
        void setLaneClass(VVMLaneClass lane_class);

        /**
         * Getter for the predecessors of this lane. Stored as a set of road id and lane id.
         * @return Predecessors of this lane.
         */
        [[nodiscard]] const std::set<std::pair<int, int>> &getPredecessors() const;

        /**
         * Setter for the predecessors of this lane. Stored as a set of road id and lane id.
         * @param predecessors New predecessors of this lane.
         */
        void setPredecessors(const std::set<std::pair<int, int>> &predecessors);

        /**
         * Add a predecessor of this lane. Stored as a set of road id and lane id.
         * @param predecessor New predecessor of this lane.
         */
        void addPredecessors(const std::pair<int, int> &predecessor);

        /**
         * Getter for the successors of this lane. Stored as a set of road id and lane id.
         * @return Successors of this lane.
         */
        [[nodiscard]] const std::set<std::pair<int, int>> &getSuccessors() const;

        /**
         * Setter for the successors of this lane. Stored as a set of road id and lane id.
         * @param successors New successors of this lane.
         */
        void setSuccessors(const std::set<std::pair<int, int>> &successors);

        /**
         * Add a successor of this lane. Stored as a set of road id and lane id.
         * @param successor New successor of this lane.
         */
        void addSuccessors(const std::pair<int, int> &successor);

        /**
         * Getter for the pointer to the right border. Points to the road id and border id.
         * @return Pointer to road id and lane id that is the right border of this lane.
         */
        [[nodiscard]] const std::pair<int, int> &getBorderRight() const;

        /**
         * Set the pointer to the right border. Points to the road id and border id.
         * @param border_right New id tuple to the road id and lane id.
         */
        void setBorderRight(const std::pair<int, int> &border_right);

        /**
         * Getter for the pointer to the right border. Points to the road id and border id.
         * @return Pointer to road id and lane id that is the left border of this lane.
         */
        [[nodiscard]] const std::pair<int, int> &getBorderLeft() const;

        /**
         * Set the pointer to the left border. Points to the road id and border id.
         * @param border_left New id tuple to the road id and lane id.
         */
        void setBorderLeft(const std::pair<int, int> &border_left);

        /**
         * Getter for the boundaries of this lane.
         * @return Boundaries of this lanes.
         */
        [[nodiscard]] Boundaries_Ptr laneBoundaries() const;

        /**
         * Adds a single lane boundary to the lane.
         * @param lane_boundary New boundary.
         */
        void addLaneBoundary(const Boundary_Ptr &lane_boundary);

        /**
         * Getter for the flat markings of this lane.
         * @return Flat markings of this lanes.
         */
        [[nodiscard]] FlatMarkings_Ptr flatMarkings() const;

        /**
         * Adds a single flatmarking to the lane.
         * @param lane_flatMarking New flatmarking.
         */
        void addFlatMarking(const FlatMarking_Ptr &lane_flatMarking);

        /**
         * Getter for the surface of this lane.
         * @return Surface of this lanes.
         */
        [[nodiscard]] Surface_Ptr laneSurface() const;

        /**
         * Getter for the layer this is on. Layer 1 indicated a permanent change and layer 3 a temporary change.
         * @return 1 if permanent and 3 if not.
         */
        [[nodiscard]] int getLayerFlag() const;

        /**
         * Setter for the layer. Layer 1 indicated permanent env. and layer 3 changes on layer 1 or 2.
         * @param layer_flag New layer.
         */
        void setLayerFlag(int layer_flag);

        friend std::ostream &operator<<(std::ostream &os, const Lane &lane);
    };

    typedef std::shared_ptr<Lane> Lane_Ptr; ///< Pointer
    typedef std::vector<Lane_Ptr> Lanes; ///< List of pointer
    typedef std::shared_ptr<Lanes> Lanes_Ptr; ///< Pointer to list of pointers
}
#endif //OMEGA_LANE_H
