from dataclasses import dataclass, field
from omega_format import DictWithProperties
from omega_format import MetaData
import re
import datetime
from ..logger import logger

def get_georeference(my_roads, header):
    """
    parse opendrive header for lat/long values (converter always assumes that lat/long values are present in header)
    :param my_roads:
    :param header: parsed header of odr file
    :return:
    """
    # default/fallback
    latitude = '50.8'
    longitude = '6.1'
    logger.info(header.geo_reference)
    if header.geo_reference:
        # Latitude
        pattern = re.compile(".*\+lat_0=(.*?)\s\+.*")
        result = pattern.findall(header.geo_reference)
        if result:
            latitude = result[0]
            latitude = latitude.replace('d', '.')
        else:
            logger.warning("Lat value was not provided in header of openDRIVE file! A default value is set.")

        # Longitude
        pattern = re.compile(".*\+lon_0=(.*?)\s\+.*")
        result = pattern.findall(header.geo_reference)
        if result:
            longitude = result[0]
            longitude = longitude.replace('d', '.')
        else:
            logger.warning("Lon value was not provided in header of openDRIVE file! A default value is set.")
    else:
        logger.warning("Header of openDRIVE file provides no geo reference. Please update!"
              " Converter takes default values for now.")

    # set lat long and converter version number and road converter version
    my_roads = my_roads.set_reference(float(latitude), float(longitude), "1.0")

    # double check
    if my_roads.meta_data.reference_point_lat is None or my_roads.meta_data.reference_point_lon is None:
        logger.error("Lat and long value needs to be provided in header of openDRIVE file")

    return my_roads


@dataclass
class Roads:
    roads_list: DictWithProperties = field(default_factory=DictWithProperties)
    meta_data: MetaData = None

    @classmethod
    def set_reference(cls, latitude, longitude, converter_version):
        meta_data = MetaData(reference_point_lat=latitude,
                             reference_point_lon=longitude,
                             road_converter_version=converter_version,
                             daytime=datetime.datetime.now(),
                             recorder_number=str(0),
                             recording_number=str(0),
                             reference_modality=6)
        self = cls(
            meta_data=meta_data,
        )
        return self

    def to_hdf5(self, hdf5_file):
        self.meta_data.to_hdf5(hdf5_file)
        # check if group road is already there (created in metadata to save road_converter_version)
        road_group = hdf5_file["road"]
        if not road_group:
            road_group = hdf5_file.create_group("road")
        self.roads_list.to_hdf5(road_group)
