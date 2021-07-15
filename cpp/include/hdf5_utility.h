/**
 * @file hdf5_utility.h
 * @authors Simon Schaefer
 * @date 16.09.2020
 *
 * This file will have all definition to interface to the h5cpp lib. The lib is only use to store data. All
 * complex interactions are handle through helper function in this file.
 *
 * Styleguide:
 *  - If the template fails for a special type of element, do not implement a loop or a special function.
 *    Implement a special definition of the template to handle the new element. This will keep the code clean and future
 *    proof.
 */

#ifndef OMEGA_HDF5_UTILITY_H
#define OMEGA_HDF5_UTILITY_H

#include <set>

#include <h5cpp/hdf5.hpp>

namespace omega {

/**
 * Template function to add a new dataset to a hdf5 group.
 * @tparam T Type of the dataset.
 * @param group Group to add dataset to.
 * @param name Name of the dataset.
 * @param element Dataset to add.
 */
    template<typename T>
    inline hdf5::node::Dataset
    add_dataset_to_group(hdf5::node::Group &group, const std::string &name, const T &element) {
        hdf5::node::Dataset dset = group.create_dataset(name, hdf5::datatype::create<T>(),
                                                        hdf5::dataspace::create(element));
        dset.write(element);
        return dset;
    }

/**
 * Special implementation of template function for std::pairs. Will be added as 1x2 vector.
 * @see add_to_group
 */
    template<>
    inline hdf5::node::Dataset add_dataset_to_group<std::pair<int, int>>(hdf5::node::Group &group,
                                                                         const std::string &name,
                                                                         const std::pair<int, int> &element) {
        // Buffer to take data.
        std::vector<int> pair_as_vector;
        // Push set to the buffer
        pair_as_vector.push_back(element.first);
        pair_as_vector.push_back(element.second);

        // Set data type to be a 1 x 2 matrix
        auto data_space = hdf5::dataspace::create(pair_as_vector);
        auto data_typ = hdf5::datatype::create<std::vector<int>>();

        // Push do hdf5
        hdf5::node::Dataset dset = group.create_dataset(name, data_typ, data_space);
        dset.write(pair_as_vector);
        return dset;
    }

/**
 * Special implementation of template function for std::set<std::pairs>. Will be added as Xx2 vector.
 * @see add_to_group
 */
    template<>
    inline hdf5::node::Dataset add_dataset_to_group<std::set<std::pair<int, int>>>(hdf5::node::Group &group,
                                                                                   const std::string &name,
                                                                                   const std::set<std::pair<int, int>> &elements) {
        // Buffer to take data.
        std::vector<std::array<int, 2>> data;

        // Push set to the buffer
        data.reserve(elements.size());
        for (auto element: elements) {
            data.push_back({{element.first, element.second}});
        }

        // Set data type to be a n x 2 matrix
        auto data_space = hdf5::dataspace::Simple({elements.size(), 2});
        auto data_typ = hdf5::datatype::create(data);

        // Push do hdf5
        hdf5::node::Dataset dset = group.create_dataset(name, data_typ, data_space);
        dset.write(data, data_typ, data_space);
        return dset;
    }

/**
 * Template function to add a new attribute to a hdf5 group.
 * @tparam T Type of the attribute.
 * @param group Group to add attribute to.
 * @param name Name of the attribute.
 * @param element Attribute to add.
 */
    template<typename T>
    void add_attribute_to_group(hdf5::node::Group &group, const std::string &name, const T &element) {
        group.attributes.create_from(name, element);
    }

    template<typename T>
    void add_attribute_to_dataset(hdf5::node::Dataset &dset, const std::string &name, const T &element) {
        dset.attributes.create(name, hdf5::datatype::create<T>(), hdf5::dataspace::create(element)).write(element);
    }

    template<typename T>
    void read_attribute(hdf5::node::Group &group, const std::string &name, T &element) {
        auto attribute = group.attributes[name];
        attribute.read(element);
    }

    template<typename T>
    void read_scalar_dataset(hdf5::node::Group &group, const std::string &name, T &element) {
        hdf5::node::Dataset dataset = group.get_dataset(name);
        dataset.read(element);
    }

    template<typename T>
    void read_dataset(hdf5::node::Group &group, const std::string &name, T &vec) {
        hdf5::node::Dataset dataset = group.get_dataset(name);
        vec.resize(dataset.dataspace().size());
        dataset.read(vec);
    }

    inline int get_group_id(const hdf5::node::Group& group) {
        std::string group_path = group.link().path().name();
        std::string id_string = group_path.substr(0, group_path.find_last_of("\\/"));
        int id = std::stoi(id_string);
        return id;
    }

    template<typename T, typename U>
    void traverse_elements_and_add_to_vector(const hdf5::node::Group& group, T &vec, U Class) {
        for (auto node: group.nodes){
            if (is_group(node)) {
                hdf5::node::Group id_group = group.get_group(node.link().path());
                std::shared_ptr<U> item = std::make_shared<U>(U::from_hdf5(id_group));
                vec->push_back(item);
            }
        }
    }
}
#endif //OMEGA_HDF5_UTILITY_H
