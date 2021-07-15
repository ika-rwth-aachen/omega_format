/**
 * @file LateralMarking.h
 * @authors Simon Schaefer
 * @date 23.09.2020
 */

#ifndef OMEGA_LATERAL_MARKING_H
#define OMEGA_LATERAL_MARKING_H

#include <set>
#include <ostream>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {
    class Road;

    typedef std::shared_ptr<Road> Road_Ptr;

/**
 * Representation of the vvm lateral marking definition.
 */
    class LateralMarking {
        int lateral_marking_id_; ///< Unique id of lateral marking. It needs to be unique within a lane.
        std::weak_ptr<Road> parent_; ///< Reference to parent

        VVMLateralMarkingType lateral_marking_type_; ///< Type of lateral marking.
        VVMLateralMarkingColor lateral_marking_color_; ///< Color of lateral marking.
        VVMLateralMarkingCondition lateral_marking_condition_; ///< Condition of lateral marking.

        std::set<std::pair<int, int>> lateral_marking_lane_ids_; ///< Lanes that are intersected with this.

        double lateral_marking_long_size_; ///< Potential depth of lateral marking.

        int layer_flag_ = 0; ///< Indicates if the changes are temporary or not. 0/1/2 = Permanent, 3 = Non-Permanent.

        /// Polyline components. All vector should have the same length.
        std::vector<double> lateral_marking_polyline_component_x_;
        std::vector<double> lateral_marking_polyline_component_y_;
        std::vector<double> lateral_marking_polyline_component_z_;

    public:
        /**
         * Write to the hdf5 file. This function will create a subgroup with the lateral_marking_id_ as name. This function
         * does not perform a check id the subgroup may already exist.
         * @param parent_group Group there the subgroup should be added to.
         * @return True if nothing went wrong, false otherwise.
         */
        bool to_hdf5(hdf5::node::Group &parent_group);

        static LateralMarking from_hdf5(hdf5::node::Group &parent_group);


        /**
         * Helper function to add a sample point to the polyline.
         * @param x X component to if the polyline sample point
         * @param y Y component to if the polyline sample point
         * @param z Z component to if the polyline sample point
         */
        void addToLateralMarkingPolyline(double x, double y, double z);

        /**
         * Getter for the lateral marking id. Should be unique within a lane.
         * @return Current lateral marking id.
         */
        [[nodiscard]] int getLateralMarkingId() const;

        /**
         * Setter for the lateral marking id. This should be a unique value. Make sure that because there are no check in
         * place.
         * @param lateral_marking_id New lateral marking id.
         */
        void setLateralMarkingId(int lateral_marking_id);

        [[nodiscard]] std::weak_ptr<Road> getParent() const;

        void setParent(const Road_Ptr &parent);

        /**
         * Getter for the lateral marking type.
         * @return Current lateral marking type.
         */
        [[nodiscard]] VVMLateralMarkingType getLateralMarkingType() const;

        /**
         * Setter for the lateral marking type.
         * @param lateral_marking_type New lateral marking type.
         */
        void setLateralMarkingType(VVMLateralMarkingType lateral_marking_type);

        /**
         * Getter for the lateral marking color.
         * @return Current lateral marking color.
         */
        [[nodiscard]] VVMLateralMarkingColor getLateralMarkingColor() const;

        /**
         * Setter for the lateral marking color.
         * @param lateral_marking_color New lateral marking color.
         */
        void setLateralMarkingColor(VVMLateralMarkingColor lateral_marking_color);

        /**
         * Getter for the lateral marking condition.
         * @return Current lateral marking condition.
         */
        [[nodiscard]] VVMLateralMarkingCondition getLateralMarkingCondition() const;

        /**
         * Setter for the lateral marking condition.
         * @param lateral_marking_type New lateral marking condition.
         */
        void setLateralMarkingCondition(VVMLateralMarkingCondition lateral_marking_condition);

        /**
         * Getter for the lateral marking depth.
         * @return Depth of lateral marking.
         */
        [[nodiscard]] double getLateralMarkingLongSize() const;

        /**
         * Setter for the lateral marking depth.
         * @param lateral marking_long_size New depth.
         */
        void setLateralMarkingLongSize(double lateral_marking_long_size);

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

        /**
         * Getter for the lanes of this lateral marking. Stored as a set of lane ids.
         * @return Lane ids of this lateral marking.
         */
        [[nodiscard]] const std::set<std::pair<int, int>> &getLanes() const;

        /**
         * Setter for the lane ids of this lateral marking. Stored as a set lane ids.
         * @param lane_ids New lane ids of this lateral marking.
         */
        void setLanes(const std::set<std::pair<int, int>> &road_lane_id_tuples);

        /**
         * Add a lane of this lateral marking. Stored as a set lane ids.
         * @param lane_id New lane id of this lateral marking.
         */
        void addLane(const std::pair<int, int> &road_lane_id_tuple);

        friend std::ostream &operator<<(std::ostream &os, const LateralMarking &marking);
    };

    typedef std::shared_ptr<LateralMarking> LateralMarking_Ptr; ///< Pointer
    typedef std::vector<LateralMarking_Ptr> LateralMarkings; ///< List of pointer
    typedef std::shared_ptr<LateralMarkings> LateralMarkings_Ptr; ///< Pointer to list of pointers
}
#endif //OMEGA_LATERAL_MARKING_H
