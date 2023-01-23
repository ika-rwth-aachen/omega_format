#include "MetaData.h"
#include "reference_types.h"
#include "hdf5_utility.h"

namespace omega {
    MetaData::MetaData() {
        formatVersion = std::string(VVMReferenceTypesSpecification().FORMAT_VERSION);

        topLevelConverterVersion = "1.3";

        refPointLong = 0.0;
        refPointLat = 0.0;
        recorderNumber = "ika";
        recordingNumber = "0";
        referenceModality = 3;
        customInformation = "";
        naturalBehavior = true;
        naturalExposure = true;
        daytime = "";
    }

    void MetaData::to_hdf5(hdf5::node::Group &parent_group) {

        omega::add_attribute_to_group(parent_group, "formatVersion", this->formatVersion);

        omega::add_attribute_to_group(parent_group, "naturalBehavior", this->naturalBehavior);
        omega::add_attribute_to_group(parent_group, "naturalExposure", this->naturalExposure);

        omega::add_attribute_to_group(parent_group, "recorderNumber", this->recorderNumber);
        omega::add_attribute_to_group(parent_group, "recordingNumber", this->recordingNumber);

        omega::add_attribute_to_group(parent_group, "refPointLat", this->refPointLat);
        omega::add_attribute_to_group(parent_group, "refPointLong", this->refPointLong);

        omega::add_attribute_to_group(parent_group, "referenceModality", this->referenceModality);
        omega::add_attribute_to_group(parent_group, "customInformation", this->customInformation);

        omega::add_attribute_to_group(parent_group, "daytime", this->daytime);

        omega::add_attribute_to_group(parent_group, "converterVersion", this->topLevelConverterVersion);
        if (parent_group.has_group("weather")) {
            hdf5::node::Group weather_group = parent_group.get_group("weather");
            omega::add_attribute_to_group(weather_group, "converterVersion", this->weatherConverterVersion);
        }
        if (parent_group.has_group("roadUser")) {
            hdf5::node::Group roadUser_group = parent_group.get_group("roadUser");
            omega::add_attribute_to_group(roadUser_group, "converterVersion", this->roadUserConverterVersion);
        }
        if (parent_group.has_group("road")) {
            hdf5::node::Group road_group = parent_group.get_group("road");
            omega::add_attribute_to_group(road_group, "converterVersion", this->roadConverterVersion);
        }
        if (parent_group.has_group("state")) {
            hdf5::node::Group state_group = parent_group.get_group("state");
            omega::add_attribute_to_group(state_group, "converterVersion", this->stateConverterVersion);
        }
        if (parent_group.has_group("miscObject")) {
            hdf5::node::Group miscObject_group = parent_group.get_group("miscObject");
            omega::add_attribute_to_group(miscObject_group, "converterVersion", this->miscObjectConverterVersion);
        }
    }

    MetaData MetaData::from_hdf5(hdf5::node::Group &parent_group) {
        MetaData meta_data = MetaData();

        read_attribute(parent_group, "formatVersion", meta_data.formatVersion);

        read_attribute(parent_group, "naturalBehavior", meta_data.naturalBehavior);
        read_attribute(parent_group, "naturalExposure", meta_data.naturalExposure);

        read_attribute(parent_group, "recorderNumber", meta_data.recorderNumber);
        read_attribute(parent_group, "recordingNumber", meta_data.recordingNumber);

        read_attribute(parent_group, "refPointLat", meta_data.refPointLat);
        read_attribute(parent_group, "refPointLong", meta_data.refPointLong);

        read_attribute(parent_group, "referenceModality", meta_data.referenceModality);
        read_attribute(parent_group, "customInformation", meta_data.customInformation);

        read_attribute(parent_group, "daytime", meta_data.daytime);

        omega::read_attribute(parent_group, "converterVersion", meta_data.topLevelConverterVersion);
        if (parent_group.has_group("weather")) {
            hdf5::node::Group weather_group = parent_group.get_group("weather");
            omega::read_attribute(parent_group, "converterVersion", meta_data.weatherConverterVersion);
        }
        if (parent_group.has_group("roadUser")) {
            hdf5::node::Group weather_group = parent_group.get_group("roadUser");
            omega::read_attribute(parent_group, "converterVersion", meta_data.roadUserConverterVersion);
        }
        if (parent_group.has_group("road")) {
            hdf5::node::Group weather_group = parent_group.get_group("road");
            omega::read_attribute(parent_group, "converterVersion", meta_data.roadConverterVersion);
        }
        if (parent_group.has_group("state")) {
            hdf5::node::Group weather_group = parent_group.get_group("state");
            omega::read_attribute(parent_group, "converterVersion", meta_data.stateConverterVersion);
        }
        if (parent_group.has_group("miscObject")) {
            hdf5::node::Group weather_group = parent_group.get_group("miscObject");
            omega::read_attribute(parent_group, "converterVersion", meta_data.miscObjectConverterVersion);
        }

        return meta_data;
    }
}