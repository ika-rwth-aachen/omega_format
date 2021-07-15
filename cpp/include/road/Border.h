/**
 * @file Border.h
 * @authors Simon Schaefer
 * @date 23.09.2020
 */

#ifndef OMEGA_BORDER_H
#define OMEGA_BORDER_H

#include <ostream>
#include <vector>

#include <h5cpp/hdf5.hpp>

namespace omega {

    class Road;

    typedef std::shared_ptr<Road> Road_Ptr;

/**
 * Representation of the vvm border. Simplified this is only a 3D polyline with an id field.
 */
    class Border {
        int border_id_; ///< Road unique id of border. Unique inside of a road.
        std::weak_ptr<Road> parent_; ///< Reference to parent

        /// Polyline components. All vector should have the same length.
        std::vector<double> border_polyline_component_x_;
        std::vector<double> border_polyline_component_y_;
        std::vector<double> border_polyline_component_z_;

    public:
        /**
         * Write to the hdf5 file. This function will create a subgroup with the border_id as name. This function does not
         * perform a check id the subgroup may already exist.
         * @param parent_group Group there the subgroup should be added to.
         * @return True if nothing went wrong, false otherwise.
         */
        bool to_hdf5(hdf5::node::Group &parent_group);
        static Border from_hdf5(hdf5::node::Group &parent_group);

        /**
         * Helper function to add a sample point to the polyline.
         * @param x X component to if the polyline sample point
         * @param y Y component to if the polyline sample point
         * @param z Z component to if the polyline sample point
         */
        void addToBorderPolyline(double x, double y, double z);

        /**
         * Getter for the current point in the component vector. Are there 0 elements, this will return 0 as well as if
         * there is 1 element. If there a two elements this will return 1 etc.
         * @return Current index in polyline.
         */
        size_t getBorderPolylineIndex();

        /**
         * Getter for the border id. This id is unique inside a road.
         * @return Border id.
         */
        [[nodiscard]] int getBorderId() const;

        /**
         * Setter for the border id. This is should be unique inside a road. The is no check performed to ensure this.
         * @param border_id New border id.
         */
        void setBorderId(int border_id);

        [[nodiscard]] std::weak_ptr<Road> getParent() const;

        void setParent(const Road_Ptr &parent);

        /**
         * Getter for the Polyline component in X-axis of the Border.
         * @return Border Polyline Component X.
         */
        std::vector<double> getBorderPolylineCompX();

        /**
         * Getter for the Polyline component in Y-axis of the Border.
         * @return Border Polyline Component Y.
         */
        std::vector<double> getBorderPolylineCompY();

        /**
         * Getter for the Polyline component in Z-axis of the Border.
         * @return Border Polyline Component Z.
         */
        std::vector<double> getBorderPolylineCompZ();

        bool operator==(Border &border);

        friend std::ostream &operator<<(std::ostream &os, const Border &border);
    };

    typedef std::shared_ptr<Border> Border_Ptr; ///< Pointer
    typedef std::vector<Border_Ptr> Borders; ///< List of pointer
    typedef std::shared_ptr<Borders> Borders_Ptr; ///< Pointer to list of pointers
}
#endif //OMEGA_BORDER_H
