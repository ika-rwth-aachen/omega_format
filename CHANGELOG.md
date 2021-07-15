# Changelog

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
