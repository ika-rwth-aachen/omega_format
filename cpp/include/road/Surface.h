/**
 * @file Surface.h
 * @authors Simon Schaefer
 * @date 23.09.2020
 */

#ifndef OMEGA_SURFACE_H
#define OMEGA_SURFACE_H

#include <ostream>
#include <vector>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {
// Class forward declarations to prevent include loops
    class Lane;

    typedef std::shared_ptr<Lane> Lane_Ptr;

/**
 * Representation of the vvm surface definition.
 */
    class Surface {
        std::weak_ptr<Lane> parent_; ///< Reference to parent

        VVMSurfaceMaterial surface_material_ = VVMSurfaceMaterial::UNKNOWN; ///< Type of surface.
        VVMSurfaceColor surface_color_ = VVMSurfaceColor::UNKNOWN; ///< Color ob surface.
        VVMSurfaceCondition surface_condition_ = VVMSurfaceCondition::NO_VALUE; ///< Condition of surface.

        int layer_flag_ = 0; ///< Indicates if the changes are temporary or not. 0/1/2 = Permanent, 3 = Non-Permanent

    public:

        /**
         * Write to the hdf5 file. This function will create a subgroup with the surface_id_ as name. This function does not
         * perform a check id the subgroup may already exist.
         * @param parent_group Group there the subgroup should be added to.
         */
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Surface from_hdf5(hdf5::node::Group &parent_group);

        [[nodiscard]] std::weak_ptr<Lane> getParent() const;

        void setParent(const Lane_Ptr &parent);

        /**
         * Getter for the surface type.
         * @return Current surface type.
         */
        [[nodiscard]] VVMSurfaceMaterial getSurfaceMaterial() const;

        /**
         * Setter for the surface material.
         * @param surface_material New surface material.
         */
        void setSurfaceMaterial(VVMSurfaceMaterial surface_material);

        /**
         * Getter for the surface color.
         * @return Current surface color.
         */
        [[nodiscard]] VVMSurfaceColor getSurfaceColor() const;

        /**
         * Setter for the surface color.
         * @param surface_color New surface color.
         */
        void setSurfaceColor(VVMSurfaceColor surface_color);

        /**
         * Getter for the surface condition.
         * @return Current surface condition.
         */
        [[nodiscard]] VVMSurfaceCondition getSurfaceCondition() const;

        /**
         * Setter for the surface condition.
         * @param surface_type New surface condition.
         */
        void setSurfaceCondition(VVMSurfaceCondition surface_condition);

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

        friend std::ostream &operator<<(std::ostream &os, const Surface &surface);
    };

    typedef std::shared_ptr<Surface> Surface_Ptr; ///< Pointer
    typedef std::vector<Surface_Ptr> Surfaces; ///< List of pointer
    typedef std::shared_ptr<Surfaces> Surfaces_Ptr; ///< Pointer to list of pointers
}
#endif //OMEGA_SURFACE_H
