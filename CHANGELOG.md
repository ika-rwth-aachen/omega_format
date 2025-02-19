# Changelog
## v4.4
- add `polygon` to dyanmic objects that contains sequence of shapely polygons over time
- rename `sub_type` to `subtype`

## v4.3
- Added converters for OpenDrive and LevelXData datasets.
- `road.idx` and `lane.idx` are now set to the object ids on calling `reference_recording.resolve()`; 
- Use pyproject.toml
- update pydantic to v2

## v4
- enum values TODO are renamed to UNKOWN, 
- recorder_id and recording_id are now strings and must be set uniuqe
- add orange light 

## v3.1
- Added customInformation and referenceModality field

## v3.0

- Introduction of attributes to save various (scalar) information (major update)
-- _.../{id}_ used in signal list to show attributes and datasets belonging to individual objects of certain types compared to information in top level class
- Erasing several groups on top level layer (due to making information to attributes)
- moving _daytime_ from _weather_ to top level
- introduced two different attributes to describe _naturalBehavior_ and _naturalExposure_. Needed in case preselected files that show _naturalBehavior_ are uploaded in the data base (those would not show _naturalExposure_).



## v2.5


- Separate converterVersion fields in Road, Dynamic Objects and Weather. Global Version number for merger
- Fixed wrong color coding excel signallist
- Renamed all _childrenID_ and _parentID_ to _overrides_ and _overriddenBy_
- Renamed _version_ to _formatVersion_
- Specification: Information that empty fields should contain a 0x0 or 0x2 
- Renamed _trafficParticipants_ to _roadUsers_
- Added lookup Table for layerFlag
- Road Object used for  Parking, deleted lane type parking
- RoadUser: moved feature detection to bounding box. Introduced _confident_ for length and width of bounding box to note down same information
