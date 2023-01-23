/**
 * @file Road.h
 * @authors Simon Schaefer
 * @date 23.09.2020
 */

#ifndef OMEGA_ROAD_H
#define OMEGA_ROAD_H

#include <vector>
#include <string>
#include <ostream>

#include <h5cpp/hdf5.hpp>

#include "vvm_definitions.h"

namespace omega {

// Class forward declarations to prevent include loops
    class Lane;

    class Border;

    class LateralMarking;

    class Sign;

    class RoadObject;

    class StructuralObject;

    typedef std::shared_ptr<Lane> Lane_Ptr;
    typedef std::vector<Lane_Ptr> Lanes;
    typedef std::shared_ptr<Lanes> Lanes_Ptr;
    typedef std::shared_ptr<Border> Border_Ptr;
    typedef std::vector<Border_Ptr> Borders;
    typedef std::shared_ptr<Borders> Borders_Ptr;
    typedef std::shared_ptr<LateralMarking> LateralMarking_Ptr;
    typedef std::vector<LateralMarking_Ptr> LateralMarkings;
    typedef std::shared_ptr<LateralMarkings> LateralMarkings_Ptr;
    typedef std::shared_ptr<Sign> Sign_Ptr;
    typedef std::vector<Sign_Ptr> Signs;
    typedef std::shared_ptr<Signs> Signs_Ptr;
    typedef std::shared_ptr<RoadObject> RoadObject_Ptr;
    typedef std::vector<RoadObject_Ptr> RoadObjects;
    typedef std::shared_ptr<RoadObjects> RoadObjects_Ptr;
    typedef std::shared_ptr<StructuralObject> StructuralObject_Ptr;
    typedef std::vector<StructuralObject_Ptr> StructuralObjects;
    typedef std::shared_ptr<StructuralObjects> StructuralObjects_Ptr;

/**
 * Class representing a road defined by the VVM definitions.
 */
    class Road {

    private:
        int road_id_ = 0; ///< Id of road used to determine the hdf group name
        VVMRoadLocation road_location_ = VVMRoadLocation::UNKNOWN; ///< Road location that indicates that the road is an urban road or not
        std::string road_name_; ///< Name of the road, use for debug and mapping reasons, not part of the vvm definition

        Lanes_Ptr lanes_; ///< List of all lanes in this road for later automatic writing
        Borders_Ptr borders_; ///< List of all borders in this road for later automatic writing
        LateralMarkings_Ptr lateral_markings_; ///< List of all lateral_marking in this road for later automatic writing
        Signs_Ptr signs_; ///< List of all sings in this road for later automatic writing
        RoadObjects_Ptr road_objects_; ///< List of all road objects in this road for later automatic writing
        StructuralObjects_Ptr structural_objects_; ///< List of all structural objects in this road for later automatic writing

    public:

        Road();

        /**
         * Will write the roads meta information in a group created on the bases of the road id. All children
         * are written as well.
         * @param parent_group Parent group, according to the vvm definition this should be the road group
         */
        bool to_hdf5(hdf5::node::Group &parent_group);

        static Road from_hdf5(hdf5::node::Group &parent_group);

        /**
         * Getter for the unique road id.
         * @return Road id.
         */
        [[nodiscard]] int getRoadId() const;

        /**
         * Setter for the road id.
         * @param road_id New road id.
         */
        void setRoadId(int road_id);

        /**
         * Getter for the road location.
         * @return Road location.
         */
        [[nodiscard]] VVMRoadLocation getRoadLocation() const;

        /**
         * Setter for the road location.
         * @param location New road location.
         */
        void setRoadLocation(VVMRoadLocation location);

        /**
         * Getter for the number of lanes.
         * @return Number of lanes.
         */
        [[nodiscard]] int getNumberOfLanes() const;

        /**
         * Getter for the road name.
         * @return Road name.
         */
        [[nodiscard]] const std::string &getRoadName() const;

        /**
         * Setter for the road name.
         * @return New road name.
         */
        void setRoadName(const std::string &road_name);

        /**
         * Getter for the lanes of this road.
         * @return List of lanes.
         */
        [[nodiscard]] Lanes_Ptr lanes() const;

        /**
         * Adds an additional lane to the list of lanes without the need of setting the hole list.
         * @param lane New lane.
         */
        void addLane(const Lane_Ptr &lane);

        /**
         * Getter for the borders of this road.
         * @return List of all borders.
         */
        [[nodiscard]] Borders_Ptr borders() const;

        /**
         * Adds an additional lane to the list of lanes without the need of setting the hole list.
         * @param lane New lane.
         */
        void addBorder(const Border_Ptr &border);

        /**
         * Getter for the lateral markings of this road.
         * @return List of all lateral markings.
         */
        [[nodiscard]] LateralMarkings_Ptr lateralMarkings() const;

        /**
         * Adds an additional lateral marking to the list of lanes without the need of setting the hole list.
         * @param lane New lane.
         */
        void addLateralMarking(const LateralMarking_Ptr &lateral_marking);

        /**
         * Getter for the signs of this road.
         * @return List of signs.
         */
        [[nodiscard]] Signs_Ptr signs() const;

        /**
         * Adds an additional sign to the list of signs without the need of setting the hole list.
         * @param sign New sign.
         */
        void addSign(const Sign_Ptr &sign);

        /**
         * Getter for the road objects of this road.
         * @return List of road objects.
         */
        [[nodiscard]] RoadObjects_Ptr roadObjects() const;

        /**
         * Adds an additional road_object to the list of road_objects without the need of setting the hole list.
         * @param road_object New road_object.
         */
        void addRoadObject(const RoadObject_Ptr &road_object);

        /**
         * Getter for the road objects of this road.
         * @return List of road objects.
         */
        [[nodiscard]] StructuralObjects_Ptr structuralObjects() const;

        /**
         * Adds an additional structural_object to the list of structural_objects without the need of setting the hole list.
         * @param structural_objects New structural_object.
         */
        void addStructuralObject(const StructuralObject_Ptr &structural_object);


        friend std::ostream &operator<<(std::ostream &os, const Road &road);
    };

    typedef std::shared_ptr<Road> Road_Ptr; ///< Pointer
    typedef std::vector<Road_Ptr> Roads; ///< List of pointer
    typedef std::shared_ptr<Roads> Roads_Ptr; ///< Pointer to list of pointers
}
#endif //OMEGA_ROAD_H
