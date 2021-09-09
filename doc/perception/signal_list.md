# PerceptionDB signal list version 3.0

| Name                   |Type (Group)          |Attribute         |Group          |Subgroup    |Signal Class            |Description                                                                                                                                                                                     |Data type                                             |unit     |Data rate           |Comment
|:-----------------------|:---------------------|:-----------------|:--------------|:-----------|:-----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------|:--------|:-------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|formatVersion|Top level|yes|||Enriched|Version number of input format used to generate this file|string|-|-|version x.y
|recorderNumber|Top level|yes|||Enriched|Number assigned to the partner performing the recording. |int|-|-|Same name can be found in scenario input format. 
|recordingNumber|Top level|yes|||Enriched|Number of recording. Together with recorder number unique filename to connect ground truth recordings with the corresponding sensor under test recordings|int|-|-|Same name can be found in scenario input format. |||||||||||
|converterVersion|Top level|yes|||Enriched|Version number of converter used to convert the data|string|-|-|Version x.y. Short documentation on converter also needs to be provided|||||||||||
|egoID|Top level|yes|||Enriched|ID of ego vehicle equiped with sensors matching the id in the DGT|int|id|-||||||||||||
|egoOffset|Top level|yes|||Enriched|Offset/delta of ego vehicle between center point and rear axle (in x-direction of vehicle coordinate system)|double|m|-|Needed to transform from global coordinate system into vehicle coordinate system|||||||||||
|customInformation|Top level|yes|||Enriched|"provide any custom information that you want the data analyzer to have| but does not fit in any of the fields below"|string|-|-||||||||||||

| Name                   |Type (Group)          |Attribute         |Group          |Subgroup    |Signal Class            |Description                                                                                                                                                                                     |Data type                                             |unit     |Data rate           |Comment
|:-----------------------|:---------------------|:-----------------|:--------------|:-----------|:-----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------|:--------|:-------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|timestamps|Top level|no|||Measured|Timestamps in seconds since beginnning of recording|double|s|-|All values that change over time have the same vector length as timestamps --> each entry in timestamps corresponds to one entry in the other vectors|||||||||||

| Name                   |Type (Group)          |Attribute         |Group          |Subgroup    |Signal Class            |Description                                                                                                                                                                                     |Data type                                             |unit     |Data rate           |Comment
|:-----------------------|:---------------------|:-----------------|:--------------|:-----------|:-----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------|:--------|:-------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|distLongitudinalValType|object|yes|||Enriched|"Provide if signal is measured by the sensor| derived manually through other information or not provided at all"|int|-|||||||||||||
|distLongitudinalVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|distLateralValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|distLateralVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|distZValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|distZVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|relVelLongitudinalValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|relVelLongitudinalVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|relVelLateralValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|relVelLateralVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|absVelLongitudinalValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|absVelLongitudinalVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|absVelLateralValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|absVelLateralVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|relAccLongitudinalValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|relAccLongitudinalVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|relAccLateralValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|relAccLateralVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|absAccLongitudinalValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|absAccLongitudinalVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|absAccLateralValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|absAccLateralVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|objectClassificationValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|objectClassificationConfidenceValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|headingValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|headingVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|widthValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|widthVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|heightValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|heightVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|lengthValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|lengthVarType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|rcsValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|ageValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|trackingPointValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|confidenceOfExistenceValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|movementClassificationValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|measStateValType|object|yes|||Enriched|"of what type is the signal (not provided, measured or determined)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||

| Name                   |Type (Group)          |Attribute         |Group          |Subgroup    |Signal Class            |Description                                                                                                                                                                                     |Data type                                             |unit     |Data rate           |Comment
|:-----------------------|:---------------------|:-----------------|:--------------|:-----------|:-----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------|:--------|:-------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|_id_|_object_||||_Measured_|_Id of detected object_|_int_|_id_|-||||||||||||
|birthStamp|object/{id}|yes|||Measured|Index in timestamps vector at birth of traffic participant (when it was first recorded by perception)|int|-|-||||||||||||
|val|object/{id}|no||distLongitudinal|Measured|Distance to center of object in ego coordinate system in longitudinal direction|double|m|25 Hz / 10 Hz|How to define ego coordinate system will be provided in specification|||||||||||
|var|object/{id}|no||distLongitudinal|Measured / Enriched|Variance of longitudinal distance|double|m^2|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||distLateral|Measured|Distance to center of object in ego coordinate system in lateral direction|double|m|25 Hz / 10 Hz|How to define ego coordinate system will be provided in specification|||||||||||
|var|object/{id}|no||distLateral|Measured / Enriched|Variance of lateral distance|double|m^2|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||distZ|Measured|Distance to center of object in ego coordinate system in z direction|double|m|25 Hz / 10 Hz|How to define ego coordinate system will be provided in specification|||||||||||
|var|object/{id}|no||distZ|Measured / Enriched|Variance of distance in z direction|double|m^2|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||relVelLongitudinal|Measured|Velocity relativ to ego in longitudinal direction|double|m/s|25 Hz / 10 Hz||||||||||||
|var|object/{id}|no||relVelLongitudinal|Measured / Enriched|variance of relativ velocity in longitudinal direction|double|m^2/s^2|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||relVelLateral|Measured|Velocity relativ to ego in lateral direction|double|m/s|25 Hz / 10 Hz||||||||||||
|var|object/{id}|no||relVelLateral|Measured / Enriched|Variance of relativ velocity in lateral direction|double|m^2/s^2|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||absVelLongitudinal|Measured|Absolute velocity of object in longitudinal direction|double|m/s|25 Hz / 10 Hz||||||||||||
|var|object/{id}|no||absVelLongitudinal|Measured / Enriched|variance of absolute velocity of object in longitudinal direction|double|m^2/s^2|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||absVelLateral|Measured|Absolute velocity of object in lateral direction|double|m/s|25 Hz / 10 Hz||||||||||||
|var|object/{id}|no||absVelLateral|Measured / Enriched|variance of absolute velocity of object in lateral direction|double|m^2/s^2|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||relAccLongitudinal|Measured|Relative acceleration in longitudinal direction|double|m/s^2|25 Hz / 10 Hz||||||||||||
|var|object/{id}|no||relAccLongitudinal|Measured / Enriched|Variance of relative acceleration in longitudinal direction|double|m^2/s^4|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||relAccLateral|Measured|Relative acceleration in lateral direction|double|m/s^2|25 Hz / 10 Hz||||||||||||
|var|object/{id}|no||relAccLateral|Measured / Enriched|Variance of relative acceleration in lateral direction|double|m^2/s^4|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||absAccLongitudinal|Measured|Absolute acceleration in longitudinal direction|double|m/s^2|25 Hz / 10 Hz||||||||||||
|var|object/{id}|no||absAccLongitudinal|Measured / Enriched|Variance of absolute acceleration in longitudinal direction|double|m^2/s^4|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||absAccLateral|Measured|Absolute acceleration in lateral direction|double|m/s^2|25 Hz / 10 Hz||||||||||||
|var|object/{id}|no||absAccLateral|Measured / Enriched|Variance of absolute acceleration in lateral direction|double|m^2/s^4|25 Hz / 10 Hz|All variances can either be measured by the used sensor or they can be used to note down that this value is not provided by the sensor. This is noted down by -1. If only the variance is not provided this is noted down by an entry of 10^5|||||||||||
|val|object/{id}|no||objectClassification|Measured|Object classification|int|-|25 Hz / 10 Hz|Lookup table will be provided|||||||||||
|confidence|object/{id}|no||objectClassification|Measured / Enriched|Classification confidence. The higher the number the more reliable is the assignment|double|-|25 Hz / 10 Hz|If not provided use -1|||||||||||
|val|object/{id}|no||heading|Measured|heading angle of target object|double|rad|25Hz / 10Hz||||||||||||
|var|object/{id}|no||heading|Measured / Enriched|variance of heading angle of target object|double|rad^2|25Hz / 10Hz||||||||||||
|val|object/{id}|no||width|Measured|width of target|double|m|25Hz / 10Hz||||||||||||
|var|object/{id}|no||width|Measured / Enriched|variance of width of target|double|m^2|25Hz / 10Hz||||||||||||
|val|object/{id}|no||height|Measured|height of target|double|m|25Hz / 10Hz||||||||||||
|var|object/{id}|no||height|Measured / Enriched|variance of height of target|double|m^2|25Hz / 10Hz||||||||||||
|val|object/{id}|no||length|Measured|length of target|double|m|25Hz / 10Hz||||||||||||
|var|object/{id}|no||length|Measured / Enriched|variance of length of target|double|m^2|25Hz / 10Hz||||||||||||
|rcs|object/{id}|no|||Measured|RCS of target|double|dBm^2|25Hz / 10Hz||||||||||||
|age|object/{id}|no|||Measured|Age of target (how long has it been tracked)|double|s|25Hz / 10Hz||||||||||||
|trackingPoint|object/{id}|no|||Measured|which tracking point/feature (3x3 grid on object) was detected|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|confidenceOfExistence|object/{id}|no|||Measured|Existance probability|double|%|25Hz / 10Hz||||||||||||
|movementClassification|object/{id}|no|||Measured / Enriched|"Classification of movement (e.g. oncoming, crossing, stationary etc.)"|int|-|25Hz / 10Hz|Lookup table will be provided|||||||||||
|measState|object/{id}|no|||Measured / Enriched|Measurement State|int |-|25Hz / 10Hz|Lookup table will be provided|||||||||||

| Name                   |Type (Group)          |Attribute         |Group          |Subgroup    |Signal Class            |Description                                                                                                                                                                                     |Data type                                             |unit     |Data rate           |Comment
|:-----------------------|:---------------------|:-----------------|:--------------|:-----------|:-----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------|:--------|:-------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Metainformation on sensor||||||||||Sensorspecification should also be provided|||||||||||
|sensorModality|sensor/{id}|yes|||Enriched|"Radar Camera Lidar Fusion etc."|int|-|-|Lookup Table will be provided|||||||||||
|fusionInformation|sensor/{id}|yes|||Enriched|In case of fusion you can provide information on the used sensor modalities here as a list|string|-|-||||||||||||
|sensorName|sensor/{id}|yes|||Enriched|Exact name of sensor|string|-|-||||||||||||
|_sensorID_|_sensor_||||_Enriched_|_Id of sensor in order to couple metainformation and object data_|_int_|-|-||||||||||||
|firmwareVersion|sensor/{id}|yes|||Enriched|Number of firmware flashed on sensor used or version number of fusion algorithm if fusion|string|-|-||||||||||||
|originalUpdaterate|sensor/{id}|yes|||Enriched|Provide the original framerate from which the data has probably be down or upsampled|double|Hz|-||||||||||||
|sensorPosLongitudinal|sensor/{id}|yes|||Measured|Mounting position of sensor relativ to ego coordinate system origin|double|m|-||||||||||||
|sensorPosLateral|sensor/{id}|yes|||Measured|Mounting position of sensor relativ to ego coordinate system origin|double|m|-||||||||||||
|sensorPosZ|sensor/{id}|yes|||Measured|Mounting position of sensor relativ to ego coordinate system origin|double|m|-||||||||||||
|sensorHeading|sensor/{id}|yes|||Measured|Orientation of the sensor in the ego coordinate system|double|degree|-||||||||||||
|sensorPitch|sensor/{id}|yes|||Measured|Orientation of the sensor in the ego coordinate system|double|degree|-||||||||||||
|sensorRoll|sensor/{id}|yes|||Measured|Orientation of the sensor in the ego coordinate system|double|degree|-||||||||||||
|maxRange|sensor/{id}|yes|||Enriched|Maximum range of sensor in short range|double|m|-||||||||||||
|minRange|sensor/{id}|yes|||Enriched|minimum range of sensor in short range|double|m|-||||||||||||
|foVVertical|sensor/{id}|yes|||Enriched|Vertical field of view|double|degree|-||||||||||||
|foVHorizontal|sensor/{id}|yes|||Enriched|Horizontal field of view|double|degree|-|Complete angle. Angle is assumed to extent equally to the left and the right hand side|||||||||||
|minVelocity|sensor/{id}|yes|||Enriched|Minimum velocity sensor can measure|double|m/s|-||||||||||||
|maxVelocity|sensor/{id}|yes|||Enriched|Maximum velocity sensor can measure|doubble|m/s|-||||||||||||
|angleResolutionVertical|sensor/{id}|yes|||Enriched|Angle resolution in vertical direction|double|degree|-||||||||||||
|angleResolutionHorizontal|sensor/{id}|yes|||Enriched|Angle resolution in horizontal direction|double|degree|-||||||||||||
|rangeResolution|sensor/{id}|yes|||Enriched|horizontal distance resolution|double|m|-|if only one value is given for distance resolution use range entry|||||||||||
|verticalResolution|sensor/{id}|yes|||Enriched|vertical distance resolution|double|m|-|if only one value is given for distance resolution use range entry|||||||||||
|velocityResolution|sensor/{id}|yes|||Enriched|velocity resolution|double|m/s|-||||||||||||
|angleAccuracy|sensor/{id}|yes|||Enriched|angel accuracy|double|degree|-||||||||||||
|verticalAccuracy|sensor/{id}|yes|||Enriched|vertical distance accuracy|double|m|-|if only one value is given for distance accuracy use range entry|||||||||||
|rangeAccuracy|sensor/{id}|yes|||Enriched|horizontal distance accuracy|double|m|-|if only one value is given for distance accuracy use range entry|||||||||||
|velocityAccuracy|sensor/{id}|yes|||Enriched|velocity distance accuracy|double|m/s|-||||||||||||
|anglePrecision|sensor/{id}|yes|||Enriched|angle precision|double|degree|-||||||||||||
|rangePrecision|sensor/{id}|yes|||Enriched|horizontal distance precision|double|m|-|if only one value is given for distance precission use range entry|||||||||||
|verticalPrecision|sensor/{id}|yes|||Enriched|vertical distance precision|double|m|-|if only one value is given for distance precission use range entry|||||||||||
|velocityPrecision|sensor/{id}|yes|||Enriched|velocity precision|double|m/s|-||||||||||||
|trackConfirmationLatency|sensor/{id}|yes|||Enriched|Time until track of new object is outputed|double|ms|-||||||||||||
|trackDropLatency|sensor/{id}|yes|||Enriched|Time until track of an object previously tracked is deleted|double|ms|-||||||||||||
|maxObjectTracks|sensor/{id}|yes|||Enriched|maximum number of objects the sensor can track|int|-|-||||||||||||

| Name                   |Type (Group)          |Attribute         |Group          |Subgroup    |Signal Class            |Description                                                                                                                                                                                     |Data type                                             |unit     |Data rate           |Comment
|:-----------------------|:---------------------|:-----------------|:--------------|:-----------|:-----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------|:--------|:-------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Ego Position||||||can be filled with GNSS data or other self-determined positioning data|||||||||||||||
|val|egoPosition|no|posLongitude||Measured||double|°E|25Hz/10Hz||||||||||||
|var|egoPosition|no|posLongitude||Measured||double||25Hz/10Hz||||||||||||
|val|egoPosition|no|posLatitude||Measured||double|°N|25Hz/10Hz||||||||||||
|var|egoPosition|no|posLatitude||Measured||double||25Hz/10Hz||||||||||||
|val|egoPosition|no|posZ||Measured||double|m|25Hz/10Hz||||||||||||
|var|egoPosition|no|posZ||Measured||||||||||||||||
|val|egoPosition|no|heading||Measured||double|deg|25Hz/10Hz||||||||||||
|var|egoPosition|no|heading||Measured||double|deg^2|25Hz/10Hz||||||||||||
|yawRate|egoPosition|no|||Measured||double|deg/s|25Hz/10Hz||||||||||||
|pitch|egoPosition|no|||Measured||double|deg|25Hz/10Hz||||||||||||

| Name                   |Type (Group)          |Attribute         |Group          |Subgroup    |Signal Class            |Description                                                                                                                                                                                     |Data type                                             |unit     |Data rate           |Comment
|:-----------------------|:---------------------|:-----------------|:--------------|:-----------|:-----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------|:--------|:-------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Additional Sensors (if vehicle equipped with such)||||||Additional sensors (if vehicle equipped with such)||||AVL considers equiping the vehicle with additional sensors for the sensor under test setup|||||||||||
|lightIntensity|MiscInfo||||Measured|light distance intensity for short range|double|lux|25Hz/10Hz|information will follow once sensor has been specified and output of it is clear|||||||||||
|acoustics|MiscInfo||||Measured|acoustics distance s for short range|double|dB|25Hz/10Hz|information will follow once sensor has been specified and output of it is clear|||||||||||
