#include "road/Sign.h"
#include "road/Road.h"
#include "hdf5_utility.h"

namespace omega {

    bool Sign::to_hdf5(hdf5::node::Group &parent_group) const {
        try {
            // Writing the hdf group to a group with id as name
            hdf5::node::Group hdf5_group(parent_group.create_group(std::to_string(this->sign_id_)));
            omega::add_attribute_to_group(hdf5_group, "type", this->sign_type_);
            omega::add_attribute_to_group(hdf5_group, "value", this->value_);
            omega::add_attribute_to_group(hdf5_group, "sizeClass", this->size_class_);
            omega::add_attribute_to_group(hdf5_group, "history", this->history_);
            omega::add_attribute_to_group(hdf5_group, "timedependent", this->time_dependent_);
            omega::add_attribute_to_group(hdf5_group, "weatherdependent", this->weather_dependent_);
            omega::add_attribute_to_group(hdf5_group, "fallback", this->fallback_);
            omega::add_dataset_to_group(hdf5_group, "overriddenBy", std::vector<int>());
            omega::add_dataset_to_group(hdf5_group, "overrides", std::vector<int>());
            omega::add_attribute_to_group(hdf5_group, "layerFlag", this->layer_flag_);
            omega::add_dataset_to_group(hdf5_group, "applicableLanes", this->applicable_lanes_);
            omega::add_dataset_to_group(hdf5_group, "connectedTo", this->connected_to_);
            omega::add_attribute_to_group(hdf5_group, "heading", this->heading_);
            // Write polyline node
            omega::add_dataset_to_group(hdf5_group, "posX", this->position_[0]);
            omega::add_dataset_to_group(hdf5_group, "posY", this->position_[1]);
            omega::add_dataset_to_group(hdf5_group, "posZ", this->position_[2]);

            // TODO Fill the empty boundary field "overrides"
            // TODO Fill the empty boundary field "overriddenBy"
            return true;
        } catch (std::exception &e) {
            return false;
        }
    }

    Sign Sign::from_hdf5(hdf5::node::Group &parent_group) {
        Sign sign;
        sign.sign_id_ = omega::get_group_id(parent_group);

        omega::read_attribute(parent_group, "type", sign.sign_type_);
        omega::read_attribute(parent_group, "value", sign.value_);
        omega::read_attribute(parent_group, "sizeClass", sign.size_class_);
        omega::read_attribute(parent_group, "history", sign.history_);
        omega::read_attribute(parent_group, "timedependent", sign.time_dependent_);
        omega::read_attribute(parent_group, "weatherdependent", sign.weather_dependent_);
        omega::read_attribute(parent_group, "fallback", sign.fallback_);
        omega::read_attribute(parent_group, "layerFlag", sign.layer_flag_);
        omega::read_attribute(parent_group, "heading", sign.heading_);

        //omega::add_dataset_to_group(parent_group, "overriddenBy", std::vector<int>());
        //omega::add_dataset_to_group(parent_group, "overrides", std::vector<int>());
        //omega::read_dataset(parent_group, "applicableLanes", sign.applicable_lanes_);
        //omega::read_dataset(parent_group, "connectedTo", sign.connected_to_);

        omega::read_scalar_dataset(parent_group, "posX", sign.position_[0]);
        omega::read_scalar_dataset(parent_group, "posY", sign.position_[1]);
        omega::read_scalar_dataset(parent_group, "posZ", sign.position_[2]);

        return sign;
    }

    int Sign::getSignId() const {
        return this->sign_id_;
    }

    void Sign::setSignId(int sign_id) {
        this->sign_id_ = sign_id;
    }

    std::weak_ptr<Road> Sign::getParent() const {
        assert(this->parent_.lock());
        return this->parent_;
    }

    void Sign::setParent(const Road_Ptr &parent) {
        this->parent_ = parent;
    }

    const std::string &Sign::getSignType() const {
        return this->sign_type_;
    }

    void Sign::setSignType(const std::string &type) {
        this->sign_type_ = type;
    }

    int Sign::getValue() const {
        return this->value_;
    }

    void Sign::setValue(int value) {
        this->value_ = value;
    }

    int Sign::getSizeClass() const {
        return this->size_class_;
    }

    void Sign::setSizeClass(int size_class) {
        this->size_class_ = size_class;
    }

    const std::string &Sign::getHistory() const {
        return this->history_;
    }

    void Sign::setHistory(const std::string &history) {
        this->history_ = history;
    }

    bool Sign::isTimeDependent() const {
        return this->time_dependent_;
    }

    void Sign::setTimeDependent(bool time_dependent) {
        this->time_dependent_ = time_dependent;
    }

    bool Sign::isWeatherDependent() const {
        return this->weather_dependent_;
    }

    void Sign::setWeatherDependent(bool weather_dependent) {
        this->weather_dependent_ = weather_dependent;
    }

    const std::set<std::pair<int, int>> &Sign::getApplicableLanes() const {
        return this->applicable_lanes_;
    }

    void Sign::setApplicableLanes(const std::set<std::pair<int, int>> &applicable_lanes) {
        this->applicable_lanes_ = applicable_lanes;
    }

    const std::set<std::pair<int, int>> &Sign::getConnectedTo() const {
        return this->connected_to_;
    }

    void Sign::setConnectedTo(const std::set<std::pair<int, int>> &connected_to) {
        this->connected_to_ = connected_to;
    }

    void Sign::addConnectedTo(const std::pair<int, int> &connected_to) {
        this->connected_to_.insert(connected_to);
    }

    bool Sign::isFallback() const {
        return this->fallback_;
    }

    void Sign::setFallback(bool fallback) {
        this->fallback_ = fallback;
    }

    double Sign::getHeading() const {
        return this->heading_;
    }

    void Sign::setHeading(double heading) {
        this->heading_ = heading;
    }

    int Sign::getLayerFlag() const {
        return this->layer_flag_;
    }

    void Sign::setLayerFlag(int layer_flag) {
        this->layer_flag_ = layer_flag;
    }

    void Sign::setPosition(double x, double y, double z) {
        this->position_[0] = x;
        this->position_[1] = y;
        this->position_[2] = z;
    }

    const double *Sign::getPosition() const {
        return position_;
    }

    const std::string &Sign::getRoadName() const {
        return road_name_;
    }

    void Sign::setRoadName(const std::string &road_name) {
        road_name_ = road_name;
    }

    std::ostream &operator<<(std::ostream &os, const Sign &sign) {
        os << "Id: " << sign.sign_id_
           << " Type: " << sign.sign_type_
           << " Value: " << sign.value_
           << " Size Class: " << sign.size_class_
           << " Position: " << sign.position_[0] << " " << sign.position_[1] << " " << sign.position_[2]
           << " Heading: " << sign.heading_;
        return os;
    }

}
