# ![](./omega_format/visualization/ui/icon.svg) OMEGAFormat - Python Library
The OMEGAFormat is a data foramt for storing reference and perception data from pilotings, test drives and simulation in urban traffic (and highway). It stores object-list-based trajectory information about dynamic objects together with map information and more. This module enables the creation, and visualization of data conforming to this data format. Additionally, it can check files for conformance and perform basic sanity checks on the data and convert data in OpenDrive and LevelXData data format into the OMEGAFormat.

The OMEGAFormat itself is specified in the [OMEGAFormat specification](https://github.com/ika-rwth-aachen/omega_format/tree/main/doc/specification.md) and [reference list of signals](https://github.com/ika-rwth-aachen/omega_format/tree/main/doc/signal_list_reference.md).

The OMEGAFormat was developed in the [German VVMethods Project](https://www.vvm-projekt.de). For a detailed insight in the role of the OMEGAFormat for Validation and Verification of Automated Driving Systems proposed by VVMethods, take a look at [Deliverable 13: Scenario-based Model of the ODD through Scenario Databases](https://www.vvm-projekt.de/securedl/sdl-eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3Mzg1NzcxNjcsImV4cCI6MTczODY2NzE2NywidXNlciI6MCwiZ3JvdXBzIjpbMCwtMV0sImZpbGUiOiJmaWxlYWRtaW4vdXNlcl91cGxvYWQvUGFwZXJzL0RlbGl2ZXJhYmxlMTMtU2NlbmFyaW8tYmFzZWRfTW9kZWxfb2ZfdGhlX09ERF90aHJvdWdoX1NjZW5hcmlvX0RhdGFiYXNlcy5wZGYiLCJwYWdlIjoyM30.gHKKVt8Ufaw54lPVu6UJAPucRkbHn822glI80KZPD0E/Deliverable13-Scenario-based_Model_of_the_ODD_through_Scenario_Databases.pdf)


Reference: [OMEGAFormat: A comprehensive format of traffic recordings for scenario extraction, Scholtes et. al 2022](https://scholar.google.com/scholar?cluster=11817504218720105408)

Check out the tutorials in `./tutorials`
- **[01_Introduction](https://github.com/ika-rwth-aachen/omega_format/tree/main/tutorials/01_Introduction.ipynb):** Introduction to using the library and basic knowledge about the OMEGAFormat.
- **[02_CLI_Usage](https://github.com/ika-rwth-aachen/omega_format/tree/main/tutorials/02_CLI_Usage.ipynb):** Examples of how to use the command line interface.
- **[03_Converters](https://github.com/ika-rwth-aachen/omega_format/tree/main/tutorials/03_Converters.ipynb):** Examples of how to convert from existing data formats into the OMEGAFormat.

# Installation
If you want an editable install (modifications to the files in the directory are immediately used by the module) run:
```
pip install -e .[visualization]
```

# Converters
The python library allows the conversion of following data formats into the OMEGAFormat.

- OpenDrive
- LevelXData [tested with inD, highD and exiD]

# Data Format
The base of both, the reference data format and the perception data format is the [HDF5](https://www.hdfgroup.org/solutions/hdf5) file format. This library utilizes [h5py](https://www.h5py.org/) to interact with those.

## Reference Data
The `OMEGAFormat reference recording` format is used to store data that represents the 'true' state of road users, infrastructure information, weather and more during a piloting, testing or simulation. The representation is on an object list basis.
The following diagram shows an overview of the hierarchy in the `OMEGAFormat reference recording` format. A more detailed description can be found in the [specification document](https://github.com/ika-rwth-aachen/omega_format/tree/main/doc/specification.md) and the [signal list](https://github.com/ika-rwth-aachen/omega_format/tree/main/doc/signal_list_reference.md).

![](https://github.com/ika-rwth-aachen/omega_format/tree/main/reference_hierarchy.PNG)

## Perception Data
The `PerceptionRecording` format is used to store data that represents what a vehicle under test, sensor under test or similar perceives from its surroundings. It is designed to be compared against the `ReferenceRecording` format. The following diagram shows an overview of the hierarchy in the `PerceptionRecording` format. A more detailed description is coming soon.

![](https://github.com/ika-rwth-aachen/omega_format/tree/main/perception_hierarchy.PNG)



# Further Help
## Standalone viewer of hdf5 files

There are plenty of tools, e.g.
- [silx](http://www.silx.org/doc/silx/latest/install.html) (also available on "Ubuntu Software")
- [ViTables](https://vitables.org/)
- [HDFView](https://www.hdfgroup.org/download-hdfview/)
- [Online-Viewer: MyHDF5](https://myhdf5.hdfgroup.org/)


## Documentation
 You can create a documentation with [pdoc3](https://pdoc3.github.io/pdoc/). To do this first install `pdoc3` with `pip install pdoc3` and then run `pdoc3 --http localhost:8889 --template-dir .\doc\templates\ .\omega_format` from the root of this repo to view the documentation in your web browser.

# License
The library is published under the MIT license specified in [LICENSE](https://github.com/ika-rwth-aachen/omega_format/tree/main/LICENSE). An overview over the licenses of the dependencies in this library is listed in [LICENSES_OF_REQUIREMENTS.md](https://github.com/ika-rwth-aachen/omega_format/tree/main/LICENSES_OF_REQUIREMENTS.md).

# Contact
In case of questions regarding the format, this repository or otherwise related feel free to raise an issue or contact Michael Schuldes (michael.schuldes@ika.rwth-aachen.de).

# Acknowledgement
This module is developed by [ika - RWTH Aachen](https://www.ika.rwth-aachen.de/de/) as a contribution to the [VVM](https://www.vvm-projekt.de/projekt) project which aims to develop test procedures and to provide frameworks and methods for the safety verification of automated vehicles. VVM is working on the use case of Urban Intersections and focuses on driving functions up to full automation of vehicles (SAE Level 4 and 5).

The research leading to these results is funded by the German Federal Ministry for Economic Affairs and Energy within the project “Verifikations- und Validierungsmethoden automatisierter Fahrzesuge im urbanen Umfeld". The authors would like to thank the consortium for the successful cooperation. 

<a href='https://www.bmwi.de/Navigation/EN/Home/home.html'><img src="bmwi_logo.gif" alt="bmwi_logo" height="200"/></a>
