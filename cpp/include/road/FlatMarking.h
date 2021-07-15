/**
 * @file FlatMarking.h
 * @authors Simon Schaefer
 * @date 26.01.2021
 */

#ifndef OMEGA_FLAT_MARKING_H
#define OMEGA_FLAT_MARKING_H

#include <ostream>
#include <vector>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

// Class forward declarations to prevent include loops
    class Lane;

    typedef std::shared_ptr<Lane> Lane_Ptr;

/**
 * Class representing a flat marking defined by the VVM definitions.
 */
    class FlatMarking {
        int flat_marking_id_ = 0;
        std::weak_ptr<Lane> parent_; ///< Reference to parent

        VVMFlatMarkingType flat_marking_type_ = VVMFlatMarkingType::NOTICE_ARROW;
        VVMFlatMarkingColor flat_marking_color_ = VVMFlatMarkingColor::UNKNOWN;
        VVMFlatMarkingCondition flat_marking_condition_ = VVMFlatMarkingCondition::UNKNOWN;
        int flat_marking_value_ = 0;

        /// Polyline components. All vector should have the same length.
        std::vector<double> flat_marking_polyline_component_x_;
        std::vector<double> flat_marking_polyline_component_y_;
        std::vector<double> flat_marking_polyline_component_z_;

        int flat_marking_layer_flag_ = 0;

        int flat_marking_related_road_ = 0;
        int flat_marking_related_lane_ = 0;

        int layer_flag_ = 0;

    public:

        virtual ~FlatMarking();

        /**
         * Write to the hdf5 file. This function will create a group with the flat marking id  as name.
         * @param parent_group Group of higher-order in which the data will be written.
         */
        bool to_hdf5(hdf5::node::Group &parent_group);

        static FlatMarking from_hdf5(hdf5::node::Group &parent_group);

        /**
         * Getter for the FlatMarking id.
         * @return Flatmarking id.
         */
        [[nodiscard]] int getFlatMarkingId() const;

        /**
         * Setter for the FlatMarking id.
         * @param flat_marking_id New Flatmarking id.
         */
        void setFlatMarkingId(int flat_marking_id);

        [[nodiscard]] std::weak_ptr<Lane> getParent() const;

        void setParent(const Lane_Ptr &parent);

        /**
         * Getter for the FlatMarking Color.
         * @return Flatmarking Color.
         */
        [[nodiscard]] VVMFlatMarkingColor getFlatMarkingColor() const;

        /**
         * Setter for the FlatMarking Color.
         * @param flat_marking_color New Flatmarking Color.
         */
        void setFlatMarkingColor(VVMFlatMarkingColor flat_marking_color);

        /**
         * Getter for the FlatMarking Condition.
         * @return Flatmarking Condition.
         */
        [[nodiscard]] VVMFlatMarkingCondition getFlatMarkingCondition() const;

        /**
         * Setter for the FlatMarking Condition.
         * @param flat_marking_condition New Flatmarking Condition.
         */
        void setFlatMarkingCondition(VVMFlatMarkingCondition flat_marking_condition);

        /**
         * Getter for the FlatMarking LayerFlag.
         * @return Flatmarking LayerFlag.
         */
        [[nodiscard]] int getFlatMarkingLayerFlag() const;

        /**
         * Setter for the FlatMarking LayerFlag.
         * @param value New Flatmarking Flag.
         */
        void setFlatMarkingLayerFlag(int value);

        /**
         * Getter for the FlatMarking related Road.
         * @return Flatmarking Road.
         */
        [[nodiscard]] int getFlatMarkingRelatedRoad() const;

        /**
         * Setter for the FlatMarkings related Road.
         * @param value New Flatmarking related Road.
         */
        void setFlatMarkingRelatedRoad(int value);

        /**
         * Getter for the FlatMarking related Lane.
         * @return Flatmarking Lane.
         */
        [[nodiscard]] int getFlatMarkingRelatedLane() const;

        /**
         * Setter for the FlatMarking related Lane.
         * @param value New Flatmarking related Lane.
         */
        void setFlatMarkingRelatedLane(int value);

        /**
         * Getter for the FlatMarking Value.
         * @return Flatmarking Value.
         */
        [[nodiscard]] int getFlatMarkingValue() const;

        /**
         * Setter for the FlatMarking Value.
         * @param value New Flatmarking Value.
         */
        void setFlatMarkingValue(int flat_marking_value);

        /**
         * Getter for the FlatMarking Type.
         * @return Flatmarking Type.
         */
        [[nodiscard]] VVMFlatMarkingType getFlatMarkingType() const;

        /**
         * Setter for the FlatMarking Type.
         * @param value New Flatmarking Type.
         */
        void setFlatMarkingType(VVMFlatMarkingType flat_marking_type);

        /**
         * Adds a value to the vector of Polyline component in X-axis of the FlatMarking.
         * @param value X component of the polyline point
         */
        void addFlatMarkingPolylineCompX(double value);

        /**
         * Adds a value to the vector of Polyline component in Y-axis of the FlatMarking.
         * @param value Y-component of the polyline point
         */
        void addFlatMarkingPolylineCompY(double value);

        /**
         * Adds a value to the vector of Polyline component in Z-axis of the FlatMarking.
         * @param value Z-component of the polyline point
         */
        void addFlatMarkingPolylineCompZ(double value);

        friend std::ostream &operator<<(std::ostream &os, const FlatMarking &flat_marking);
    };

    typedef std::shared_ptr<FlatMarking> FlatMarking_Ptr; ///< Pointer
    typedef std::vector<FlatMarking_Ptr> FlatMarkings; ///< List of pointer
    typedef std::shared_ptr<FlatMarkings> FlatMarkings_Ptr; ///< Pointer to list of pointers
}
#endif // OMEGA_FLAT_MARKING_H
