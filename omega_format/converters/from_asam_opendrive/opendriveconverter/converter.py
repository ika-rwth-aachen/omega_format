from .elements.roads import Roads, get_georeference
from .elements.road import process_road
from .elements.junction import setup_connections, find_corresponding_roads, find_junction_xessor_roads
from .elements.signals import setup_signal_references
from tqdm.auto import tqdm
from .logger import logger

def convert_opendrive(my_opendrive, step_size, junction_id=None):
    """
    Converts the opendrive XML input into a OMEGAFormat road network
    :param my_opendrive: opendrive XML
    :param step_size: resolution in which the maps points are sampled in meters
    :param junction_id: if set to a value (other than None), the conversion process will be restricted to the roads
                        that are part of the specified junction and their direct predecessors
    :return: returns the road network
    """

    # create roads object and set geo reference
    my_roads = Roads()
    my_roads = get_georeference(my_roads, my_opendrive.header)

    # find certain junction by id and all attached roads
    junction_whitelist = []
    if junction_id:
        junction_whitelist = find_corresponding_roads(my_opendrive.junctions, junction_id)
        junction_whitelist = find_junction_xessor_roads(my_opendrive, junction_whitelist)

    # tables needed for matching their ids in open drive to VVM format since many connections can only be set later
    lookup_table = []   # [road id | lane_section | laneID | road id VVM | lane id VVM]
    reference_table = []    # [omega signal id | omega road id | odr signal id | odr reference id | odr connected_to id]

    logger.info(f'Starting conversion of {len(my_opendrive.roads)} opendrive roads into OMEGAFormat.')
    with tqdm(total=len(my_opendrive.roads), desc='roads', leave=False) as progress:

        # loop over individual opendrive roads and add them to omega roads dictionary in my_roads
        for road in my_opendrive.roads:
            # filter for a certain junction and attached roads
            if junction_id:
                if int(road.id) not in junction_whitelist:
                    continue

            my_roads, lookup_table, reference_table = process_road(my_roads, road, my_opendrive, step_size, lookup_table, reference_table)
            progress.update(1)

        # setting up road network information via connections and references
        logger.info('Setting up roads connections.')
        my_roads = setup_connections(my_roads, lookup_table, my_opendrive)

        # setting up signal references via references and connected_to
        logger.info('Setting up signal references.')
        my_roads = setup_signal_references(my_roads, reference_table)

        return my_roads
