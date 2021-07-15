/**
 * @file Sign.h
 * @authors Simon Schaefer
 * @date 23.09.2020
 */

#ifndef OMEGA_SIGN_H
#define OMEGA_SIGN_H

#include <set>
#include <ostream>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {
// Class forward declarations to prevent include loops
    class Road;

    typedef std::shared_ptr<Road> Road_Ptr;

/**
 * Representation of the vvm sign definition.
 */
    class Sign {
        int sign_id_ = 0; ///< Unique sign id. This value is unique inside a road.
        std::weak_ptr<Road> parent_; ///< Reference to parent

        std::string road_name_; ///< Road name for later assignment.
        std::string sign_type_; ///< Type of the sign.
        int value_ = 0; ///< Indicates the value if needed, e.g. max speed or distance.
        int size_class_ = 0; ///< Indication of the max velocity of the road, possible values are 1,2,3.
        std::string history_; ///< History of the sign if is was changed in the past. Comma separated types.
        bool time_dependent_ = false; ///< Flag that indicates that this signs is only valid for time period.
        bool weather_dependent_ = false; ///< Flag that indicates that this signs is only valid for some weather conditions.
        std::set<std::pair<int, int>> applicable_lanes_; ///< Lanes that are meant with this.
        std::set<std::pair<int, int>> connected_to_; ///< Indicates to what other sign this is related. Road and sign id.
        bool fallback_ = false; ///< Flag to indicate that this sign is only used if another system is out of order.

        /// Polyline components. All vector should have the same length.
        double position_[3] = {0.0, 0.0, 0.0};

        double heading_ = 0.0; ///< Heading angle of the sign.

        int layer_flag_ = 0; ///< Indicates if the changes are temporary or not. 0/1/2 = Permanent, 3 = Non-Permanent.

    public:

        /**
         * Write to the hdf5 file. This function will create a subgroup with the surface_id_ as name. This function does not
         * perform a check id the subgroup may already exist.
         * @param parent_group Group there the subgroup should be added to.
         */
        bool to_hdf5(hdf5::node::Group &parent_group) const;

        static Sign from_hdf5(hdf5::node::Group &parent_group);

        /**
         * Getter for the sign id. Unique inside a road. There is no check performed to ensure this.
         * @return Unique sign id.
         */
        [[nodiscard]] int getSignId() const;

        /**
         * Setter for the sign id. Should be unique inside a lane. This has to be ensured out side of this class.
         * @param sign_id Unique sign id.
         */
        void setSignId(int sign_id);

        [[nodiscard]] std::weak_ptr<Road> getParent() const;

        void setParent(const Road_Ptr &parent);

        /**
         * Getter for the sing type.
         * @return Sign type.
         */
        [[nodiscard]] const std::string &getSignType() const;

        /**
         * Setter for the sign type.
         * @param type New sign type.
         */
        void setSignType(const std::string &type);

        /**
         * Getter for the values if the sign. Does not necessarily has one. No defined behaviour of not.
         * @return Value of the sign.
         */
        [[nodiscard]] int getValue() const;

        /**
         * Setter for the sign values.
         * @param value New sign value.
         */
        void setValue(int value);

        /**
         * Getter for the sign classes.
         * @return 1,2 or 3 depending on the max vel on the lane.
         */
        [[nodiscard]] int getSizeClass() const;

        /**
         * Setter for the sign class. 1, 2, 3, Possible values.
         * @param size_class New sign class.
         */
        void setSizeClass(int size_class);

        /**
         * History of the sign of known. Comma separated string list.
         * @return Comma separated history of the sign.
         */
        [[nodiscard]] const std::string &getHistory() const;

        /**
         * Setter for the sign history.
         * @param history New sign history.
         */
        void setHistory(const std::string &history);

        /**
         * Getter for the flag indicating that this time is only valid in some time periods.
         * @return True if time dependent and false otherwise.
         */
        [[nodiscard]] bool isTimeDependent() const;

        /**
         * Setter for the time dependent flag.
         * @param time_dependent Should be true if time dependent.
         */
        void setTimeDependent(bool time_dependent);

        /**
         * Getter for the flag that indicates that this sign is only valid of certain weather condition are present.
         * @return True of sign is weather dependent.
         */
        [[nodiscard]] bool isWeatherDependent() const;

        /**
         * Setter for the weather dependent flag.
         * @param weather_dependent New weather dependent flag.
         */
        void setWeatherDependent(bool weather_dependent);

        /**
         * Getter for the lanes that this sign is applied to.
         * @return List of road to lane ids that are applied by this sign.
         */
        [[nodiscard]] const std::set<std::pair<int, int>> &getApplicableLanes() const;

        /**
         * Setter for the lanes that are applied by this sign.
         * @param applicable_lanes List of road and lane ids of lanes.
         */
        void setApplicableLanes(const std::set<std::pair<int, int>> &applicable_lanes);

        /**
         * Getter for the connection of this sign to other sign.
         * @return Connections to other sign in form of a list of road and sign id.
         */
        [[nodiscard]] const std::set<std::pair<int, int>> &getConnectedTo() const;

        /**
         * Setter for the connections of this sign to other signs.
         * @param connected_to New connections as a list of road and sign ids.
         */
        void setConnectedTo(const std::set<std::pair<int, int>> &connected_to);

        void addConnectedTo(const std::pair<int, int> &connected_to);

        /**
         * Getter for the flag that indicates, that this is only a fallback for some other kind of regulation system.
         * @return True if fallback, false otherwise.
         */
        [[nodiscard]] bool isFallback() const;

        /**
         * Setter for the fallback flag of this sign.
         * @param fallback New fallback flag.
         */
        void setFallback(bool fallback);

        /**
         * Getter for the heading angle of the sign. Indicating the angle between x axis and sign normal.
         * @return Heading angle of the sign.
         */
        [[nodiscard]] double getHeading() const;

        /**
         * Setter for the heading angle of the sign.
         * @param heading New heading angle.
         */
        void setHeading(double heading);

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
         * Setter for the position of the sign.
         * @param x X-Component of the position.
         * @param y Y-Component of the position.
         * @param z Z-Component of the position.
         */
        void setPosition(double x, double y, double z);

        /**
         * Getter for the position of the sign.
         * @return Position of sign.
         */
        [[nodiscard]] const double *getPosition() const;

        /**
         * Setter for the road name that the sign is assigned to. This road need to exist in the hdf5 structure or undefined
         * behaviour may occur.
         * @param road_name Name of the road.
         */
        void setRoadName(const std::string &road_name);

        /**
         * Getter for the road name the sign is assigned to.
         * @return Road name.
         */
        [[nodiscard]] const std::string &getRoadName() const;

        friend std::ostream &operator<<(std::ostream &os, const Sign &sign);
    };

    typedef std::shared_ptr<Sign> Sign_Ptr; ///< Pointer
    typedef std::vector<Sign_Ptr> Signs; ///< List of pointer
    typedef std::shared_ptr<Signs> Signs_Ptr; ///< Pointer to list of pointers
}
#endif //OMEGA_SIGN_H
