/**
 * @file StructuralObject.h
 * @authors Simon Schaefer
 * @date 09.02.2021
 */

#ifndef OMEGA_STRUCTURAL_OBJECT_H
#define OMEGA_STRUCTURAL_OBJECT_H

#include <set>
#include <ostream>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {
// Class forward declarations to prevent include loops
    class Road;

    typedef std::shared_ptr<Road> Road_Ptr;

/**
 * Representation of the vvm surface definition.
 */
    class StructuralObject {
        int structural_object_id_ = 0; ///< Unique structural_object id. This value is unique inside a road.
        std::weak_ptr<Road> parent_; ///< Reference to parent

        VVMStructuralObjectType
                structural_object_type_ = VVMStructuralObjectType::NOT_DECLARED; ///< Type of the structural_object.

        double structural_object_height_; ///< Potential height of object. (line -> height = 0, wall -> height != 0)

        /// Polyline components. All vector should have the same length.
        std::vector<double> polyline_component_x_;
        std::vector<double> polyline_component_y_;
        std::vector<double> polyline_component_z_;

        int layer_flag_ = 0; ///< Indicates if the changes are temporary or not. 0/1/2 = Permanent, 3 = Non-Permanent.

    public:

        /**
         * Write to the hdf5 file. This function will create a subgroup with the surface_id_ as name. This function does not
         * perform a check id the subgroup may already exist.
         * @param parent_group Group there the subgroup should be added to.
         */
        bool to_hdf5(hdf5::node::Group &parent_group) const;

        static StructuralObject from_hdf5(hdf5::node::Group &parent_group);

        /**
         * Getter for the structural_object id. Unique inside a road. There is no check performed to ensure this.
         * @return Unique structural_object id.
         */
        [[nodiscard]] int getStructuralObjectId() const;

        /**
         * Setter for the structural_object id. Should be unique inside a lane. This has to be ensured out side of this class.
         * @param structural_object_id Unique structural_object id.
         */
        void setStructuralObjectId(int structural_object_id);

        [[nodiscard]] std::weak_ptr<Road> getParent() const;

        void setParent(const Road_Ptr &parent);

        /**
         * Getter for the road object type. Returns the type of this road object.
         * @return Type of road object.
         */
        [[nodiscard]] VVMStructuralObjectType getStructuralObjectType() const;

        /**
         * Setter for the road object type. Type of the road object.
         * @param structural_object_type
         */
        void setStructuralObjectType(VVMStructuralObjectType structural_object_type);

        /**
         * Getter for the road object height. In meter and 0 means flat.
         * @return Height of the road object.
         */
        [[nodiscard]] double getStructuralObjectHeight() const;

        /**
         * Setter for the road object height. Should be positive and in meter, 0 means flat.
         * @param structural_object_height New object height.
         */
        void setStructuralObjectHeight(double structural_object_height);

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
         * Helper function to add a sample point to the polyline.
         * @param x X component to if the polyline sample point
         * @param y Y component to if the polyline sample point
         * @param z Z component to if the polyline sample point
         */
        void addToStructuralObjectPolyline(double x, double y, double z);

        friend std::ostream &operator<<(std::ostream &os, const StructuralObject &object);
    };

    typedef std::shared_ptr<StructuralObject> StructuralObject_Ptr; ///< Pointer
    typedef std::vector<StructuralObject_Ptr> StructuralObjects; ///< List of pointer
    typedef std::shared_ptr<StructuralObjects> StructuralObjects_Ptr; ///< Pointer to list of pointers
}
#endif //OMEGA_STRUCTURAL_OBJECT_H
