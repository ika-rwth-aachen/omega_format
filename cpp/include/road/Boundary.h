/**
 * @file Boundary.h
 * @authors Simon Schaefer
 * @date 23.09.2020
 */

#ifndef OMEGA_BOUNDARY_H
#define OMEGA_BOUNDARY_H

#include <ostream>
#include <vector>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

// Class forward declarations to prevent include loops
    class Lane;

    class Border;

    typedef std::shared_ptr<Lane> Lane_Ptr;
    typedef std::shared_ptr<Border> Border_Ptr;

/**
 * Representation of the vvm boundary definition.
 */
    class Boundary {
        int boundary_id_ = 0; ///< Unique id of boundary. It needs to be unique within a lane.
        std::weak_ptr<Lane> parent_; ///< Reference to parent

        VVMBoundaryType boundary_type_ = VVMBoundaryType::TODO; ///< Type of boundary. (line, wall etc.)
        VVMBoundarySubType boundary_sub_type_ = VVMBoundarySubType::TODO; ///< Subtype of the boundary. (dashed, wood etc.)
        VVMBoundaryColor boundary_color_ = VVMBoundaryColor::UNKNOWN; ///< Color ob boundary. (white, yellow etc.)
        VVMBoundaryCondition boundary_condition_ = VVMBoundaryCondition::UNKNOWN; ///< Condition of boundary. ( Fine etc.)

        bool boundary_is_on_right_side_ = false; ///< Flag to indicate that the border is on the passenger side.
        double boundary_height_ = 0.0; ///< Potential height of boundary. (line -> height = 0, wall -> height != 0)

        int poly_index_start_ = -1; ///< Starting point on the border polyline of the lane.
        int poly_index_end_ = -1; ///< Stopping point on the border polyline of the lane.

        int layer_flag_ = 0; ///< Indicates if the changes are temporary or not. 0/1/2 = Permanent, 3 = Non-Permanent

    public:
        /**
         * Write to the hdf5 file. This function will create a subgroup with the boundary_id_ as name. This function does not
         * perform a check id the subgroup may already exist.
         * @param parent_group Group there the subgroup should be added to.
         * @return True if nothing went wrong, false otherwise.
         */
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Boundary from_hdf5(hdf5::node::Group &parent_group);


        /**
         * Getter for the boundary id. Should be unique within a lane.
         * @return Current boundary id.
         */
        [[nodiscard]] int getBoundaryId() const;

        /**
         * Setter for the boundary id. This should be a unique value. Make sure that because there are no check in place.
         * @param boundary_id New boundary id.
         */
        void setBoundaryId(int boundary_id);

        [[nodiscard]] std::weak_ptr<Lane> getParent() const;

        void setParent(const Lane_Ptr &parent);

        /**
         * Getter for the boundary type.
         * @return Current boundary type.
         */
        [[nodiscard]] VVMBoundaryType getBoundaryType() const;

        /**
         * Setter for the boundary type.
         * @param boundary_type New boundary type.
         */
        void setBoundaryType(VVMBoundaryType boundary_type);

        /**
         * Getter for the boundary sub type.
         * @return Current boundary sub type.
         */
        [[nodiscard]] VVMBoundarySubType getBoundarySubType() const;

        /**
         * Setter for the boundary sub type.
         * @param boundary_sub_type New boundary sub type.
         */
        void setBoundarySubType(VVMBoundarySubType boundary_sub_type);

        /**
         * Getter for the boundary color.
         * @return Current boundary color.
         */
        [[nodiscard]] VVMBoundaryColor getBoundaryColor() const;

        /**
         * Setter for the boundary color.
         * @param boundary_color New boundary color.
         */
        void setBoundaryColor(VVMBoundaryColor boundary_color);

        /**
         * Getter for the boundary condition.
         * @return Current boundary condition.
         */
        [[nodiscard]] VVMBoundaryCondition getBoundaryCondition() const;

        /**
         * Setter for the boundary condition.
         * @param boundary_type New boundary condition.
         */
        void setBoundaryCondition(VVMBoundaryCondition boundary_condition);

        /**
         * Getter for the boundary side flag that indicates that the boundary is on the passenger side.
         * @return True if boundary is on the passenger side, false otherwise.
         */
        [[nodiscard]] bool isBoundaryIsOnRightSide() const;

        /**
         * Setter for the boundary right side flag. This flag indicates if the boundary is on the passenger side.
         * @param boundary_is_on_right_side New flag.
         */
        void setBoundaryIsOnRightSide(bool boundary_is_on_right_side);

        /**
         * Getter for the boundary height. A height of 0 indicates a flat or virtual marking.
         * @return Height of boundary or 0.
         */
        [[nodiscard]] double getBoundaryHeight() const;

        /**
         * Setter for the boundary height. This indicates the height, a height of 0 means flag markings.
         * @param boundary_height New height.
         */
        void setBoundaryHeight(double boundary_height);

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
         * Getter for the starting point on the border polyline.
         * @return Staring point on polyline.
         */
        [[nodiscard]] int getPolyIndexStart() const;

        /**
         * Setter for the polyline start index that indicates the start on the border polyline from the lane.
         * @param poly_index_start New staring point.
         */
        void setPolyIndexStart(int poly_index_start);

        /**
         * Getter for the ending point on the border polyline.
         * @return Ending point on polyline.
         */
        [[nodiscard]] int getPolyIndexEnd() const;

        /**
         * Setter for the polyline end index that indicates the end on the border polyline from the lane.
         * @param poly_index_end New ending point.
         */
        void setPolyIndexEnd(int poly_index_end);

        friend std::ostream &operator<<(std::ostream &os, const Boundary &boundary);
    };

    typedef std::shared_ptr<Boundary> Boundary_Ptr; ///< Pointer
    typedef std::vector<Boundary_Ptr> Boundaries; ///< List of pointer
    typedef std::shared_ptr<Boundaries> Boundaries_Ptr; ///< Pointer to list of pointers
}
#endif //OMEGA_BOUNDARY_H
