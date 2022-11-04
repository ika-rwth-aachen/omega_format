#include "ReferenceRecording.h"

#include <filesystem>
#include <boost/filesystem.hpp>

#include "hdf5_utility.h"

using namespace std;

template<typename L, typename V>
bool contains(L list, V value) {
    return list.find(value) != list.end();
}

namespace omega {

    ReferenceRecording::ReferenceRecording() {
        this->roads_ = std::make_shared<Roads>();
    }

    bool ReferenceRecording::to_hdf5(const std::string &output_path) {
        // Create target directory and file
        std::string path_without_filename = output_path.substr(0, output_path.find_last_of("\\/"));
        std::filesystem::create_directories(path_without_filename);
        hdf5::file::File hdf5_file = hdf5::file::create(output_path, hdf5::file::AccessFlags::TRUNCATE);

        // Create main group and write meta data
        hdf5::node::Group hdf5_group_root = hdf5_file.root();
        // Convert version to std::string to that the template works correctly
        std::string file_format_version = std::string(VVMReferenceTypesSpecification().FORMAT_VERSION);

        // Create road subgroup and write meta data
        if (!this->roads_->empty()){
            hdf5::node::Group hdf5_group_road = hdf5::node::Group(hdf5_group_root.create_group("road"));
            // Start cascaded process to write hdf5 file
            for (const auto &road: *this->roads_) {
                road->to_hdf5(hdf5_group_road);
            }
        }

        // write road users
        if (!this->roadUsers_.empty()) {
            hdf5::node::Group road_user_group = hdf5::node::Group(hdf5_group_root.create_group("dynamicObjects"));
            for (auto &road_user: this->roadUsers_) {
                //hdf5::node::Group road_user_id_group = hdf5::node::Group(
                //        road_user_group.create_group(to_string(road_user.getId())));
                road_user.to_hdf5(road_user_group);
            }
        }

        // write misc object
        hdf5::node::Group misc_object_group = hdf5::node::Group(hdf5_group_root.create_group("dynamicObjects"));
        if (false && !this->miscObjects_.has_value()) {
            for (auto &misc_objects: *this->miscObjects_) {
                misc_objects.to_hdf5(misc_object_group);
            }
        }

        if (this->weather_.has_value()) {
            hdf5::node::Group weather_group = hdf5::node::Group(hdf5_group_root.create_group("weather"));
            this->weather_->to_hdf5(weather_group);
        }

        // Writing meta information, needs to be at the end!!
        this->metaData_.to_hdf5(hdf5_group_root);
        add_dataset_to_group(hdf5_group_root, "timestamps", this->timestamps_);

        // write state
        hdf5::node::Group state_group = hdf5::node::Group(hdf5_group_root.create_group("state"));

        return true;
    }

    ReferenceRecording ReferenceRecording::from_hdf5(const std::string &input_path) {
        ReferenceRecording reference_recording;

        boost::filesystem::path file_path(input_path);
        hdf5::file::File f = hdf5::file::open(file_path, hdf5::file::AccessFlags::READWRITE);
        hdf5::node::Group root_group = f.root();

        // read meta data
        reference_recording.metaData_ = MetaData::from_hdf5(root_group);

        // read timestamps
        read_dataset(root_group, "timestamps", reference_recording.timestamps_);

        // read road users
        if (root_group.has_group("roadUser")) {
            hdf5::node::Group road_user_group = root_group.get_group("roadUser");
            for (auto node: road_user_group.nodes) {
                if (is_group(node)) {
                    hdf5::node::Group road_user_id_group = road_user_group.get_group(node.link().path());
                    RoadUser road_user = RoadUser::from_hdf5(road_user_id_group);
                    reference_recording.roadUsers_.push_back(road_user);
                }
            }
        }

        // read misc object
        if (root_group.has_group("miscObject")){
            hdf5::node::Group miscObject_group = root_group.get_group("miscObject");
            for (auto node: miscObject_group.nodes){
                if (is_group(node)) {
                    hdf5::node::Group misc_object_id_group = miscObject_group.get_group(node.link().path());
                    MiscObject miscObject = MiscObject::from_hdf5(misc_object_id_group);
                    reference_recording.miscObjects_->push_back(miscObject);
                }
            }
        }

        // read road
        if (root_group.has_group("road")) {
            hdf5::node::Group road_group = root_group.get_group("road");
            for (auto node: road_group.nodes) {
                if (is_group(node)) {
                    hdf5::node::Group road_id_group = road_group.get_group(node.link().path());
                    shared_ptr<Road> road = make_shared<Road>(Road::from_hdf5(road_id_group));
                    reference_recording.roads_->push_back(road);
                }
            }
        }

        // read weather
        if (root_group.has_group("weather")) {
            hdf5::node::Group weather_group = root_group.get_group("weather");
            reference_recording.weather_ = Weather::from_hdf5(weather_group);
        }

        return reference_recording;
    }


}
