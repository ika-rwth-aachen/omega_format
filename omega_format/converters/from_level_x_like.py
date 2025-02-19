import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import typer
from tqdm.auto import tqdm

import omega_format
from omega_format import DictWithProperties, ReferenceElement
from omega_format.converters.from_asam_opendrive import opendrive2roads

warnings.filterwarnings("ignore", category=DeprecationWarning)

app = typer.Typer()

bound_solid = omega_format.enums.reference_types.BoundaryType.SOLID
bound_dashed = omega_format.enums.reference_types.BoundaryType.DASHED


def parse_highD_road(recMeta, tracks):
    
    roads = DictWithProperties()
    for rid, direction in enumerate(['upperLaneMarkings','lowerLaneMarkings']):
        markings = [float(o) for o in recMeta.iloc[0][direction].split(';')]
        borders = DictWithProperties()
        for i, m in enumerate(markings):
            borders[i] = omega_format.road.Border(polyline=omega_format.geometry.polyline.Polyline(pos_x=np.array([tracks.x.max()+10,tracks.x.max(),tracks.x.min(),tracks.x.min()-10]),
                                                    pos_y=np.ones(4)*m,
                                                    pos_z=np.zeros(4)
                                                   )
                                    )
        border_ids = list(borders.keys())
        lanes = DictWithProperties()
        for i, (upper, lower) in enumerate(zip(border_ids[:-1],border_ids[1:])):
            right_border_id = (lower if direction=='lowerLaneMarkings' else upper)
            left_border_id = (upper if direction=='lowerLaneMarkings' else lower)
            lanes[i] = omega_format.road.Lane(
                border_right=ReferenceElement([rid,right_border_id], omega_format.Border),
                border_left=ReferenceElement([rid,left_border_id], omega_format.Border),
                type=omega_format.enums.reference_types.LaneType.DRIVING,
                subtype=omega_format.enums.reference_types.LaneSubType.UNKNOWN,
                classification=omega_format.enums.reference_types.LaneClass.NONE,
                border_right_is_inverted=direction=='lowerLaneMarkings',
                border_left_is_inverted=direction=='lowerLaneMarkings',
                boundaries=DictWithProperties({0: omega_format.Boundary(poly_index_start=0, poly_index_end=3, is_right_boundary=True,
                                                                        color=omega_format.enums.reference_types.BoundaryColor.WHITE,
                                                                        condition=omega_format.enums.reference_types.BoundaryCondition.FINE,
                                                                        type=bound_dashed if right_border_id not in [border_ids[0],border_ids[-1]] else bound_solid,
                                                                        subtype=omega_format.enums.reference_types.BoundarySubType.THICK,), 
                                               1: omega_format.Boundary(poly_index_start=0, poly_index_end=3, is_right_boundary=False,
                                                                        color=omega_format.enums.reference_types.BoundaryColor.WHITE,
                                                                        condition=omega_format.enums.reference_types.BoundaryCondition.FINE,
                                                                        type=bound_dashed if left_border_id not in [border_ids[0],border_ids[-1]] else bound_solid,
                                                                        subtype=omega_format.enums.reference_types.BoundarySubType.THICK,)})
            )
        roads[rid] = omega_format.Road(
            lanes=lanes,
            borders=borders,
            location=omega_format.enums.reference_types.RoadLocation.HIGHWAY
        )
    return roads

collumn_mapping = {
    'highd': {
        'trackId': 'id',
        'recordingId': 'id'
    },
    'inD': {
        'trackId': 'trackId',
        'recordingId': 'recordingId'
    }
}
ru = omega_format.enums.reference_types
type_mapping = {
    'Car': ru.RoadUserType.CAR,
    'Truck': ru.RoadUserType.TRUCK,
    'car': ru.RoadUserType.CAR,
    'truck_bus': ru.RoadUserType.TRUCK,
    'bicycle': ru.RoadUserType.BICYCLE,
    'pedestrian': ru.RoadUserType.PEDESTRIAN,
    'van': ru.RoadUserType.TRUCK,
    'truck': ru.RoadUserType.TRUCK
}

def get_pos_and_heading(track_of_road_user, road_user, is_highd=False):
    if is_highd:
        return dict(
            pos_x=(track_of_road_user['x']+track_of_road_user['width']/2).to_numpy(),
            pos_y=(track_of_road_user['y']+track_of_road_user['height']/2).to_numpy(),
            pos_z=np.zeros(len(track_of_road_user)),
            heading=180*np.ones(len(track_of_road_user))*(road_user.drivingDirection==1)
        )
    else:
        return dict(
            pos_x=track_of_road_user['xCenter'].to_numpy(), 
            pos_y=track_of_road_user['yCenter'].to_numpy(), 
            pos_z=np.zeros(len(track_of_road_user)),
            heading=track_of_road_user['heading'].to_numpy()
        )
        
def convert_from_levelx_like(recMeta, tracksMeta, tracks):
    if 'id' in tracks.columns:
        is_highd = True
        cm = collumn_mapping['highd']
    else:
        is_highd = False
        cm = collumn_mapping['inD']
    
    road_users = DictWithProperties()
    for idx, (_, road_user) in tqdm(list(enumerate(tracksMeta.iterrows())),leave=False):
        track_of_road_user = tracks[tracks[cm['trackId']]==road_user[cm['trackId']]]
        tr = omega_format.dynamics.trajectory.Trajectory(
            **get_pos_and_heading(track_of_road_user, road_user, is_highd),
            vel_longitudinal=track_of_road_user['xVelocity'].to_numpy(),
            vel_lateral=track_of_road_user['yVelocity'].to_numpy(),
            acc_longitudinal=track_of_road_user['xAcceleration'].to_numpy(),
            acc_lateral=track_of_road_user['yAcceleration'].to_numpy()
        )
        bb = np.ones(3)
        if is_highd:
            bb[:2] = road_user[['width','height']].to_numpy()
        else:
            bb[:2] = road_user[['length', 'width']].to_numpy() 
            if np.all(bb[:2]==0):
                if road_user['class'] == 'bicycle':
                    bb[:2] = [2,1]
                elif road_user['class'] == 'pedestrian':
                    bb[:2] = [.5, .5]
        bb = omega_format.dynamics.bounding_box.BoundingBox(vec=bb)
        road_users[f'RU({road_user[cm["trackId"]]})'] = omega_format.RoadUser(bb=bb, tr=tr, birth=road_user.initialFrame , subtype=ru.RoadUserSubTypeGeneral.REGULAR, type=type_mapping[road_user['class']], connected_to=ReferenceElement(-1, omega_format.RoadUser))
    if is_highd:
        start_time = datetime.strptime(str(recMeta.iloc[0].startTime) + ' ' + str(recMeta.iloc[0].month) + ' ' + str(recMeta.iloc[0].weekDay), '%H:%M %m.%Y %a')
    else:
        try:
            start_time = datetime.strptime(str(recMeta.iloc[0].startTime) + ' ' + str(recMeta.iloc[0].weekday), '%H %A')
        except ValueError:
            try:
                start_time = datetime.strptime(str(recMeta.iloc[0].weekday), '%A')
            except ValueError:
                 start_time = datetime.strptime(str(recMeta.iloc[0].weekday[:-1]), '%A')
    meta = omega_format.MetaData(daytime=start_time,
                                recorder_number="ika",                                recording_number=str(recMeta.iloc[0][cm['recordingId']]),
                                reference_point_lat=0,
                                reference_point_lon=0,
                                reference_modality=3,
                                natural_behavior=True,
                                natural_exposure=True,)
    reference = omega_format.ReferenceRecording(road_users=road_users,
                                                timestamps=tracks.frame.unique()/recMeta.iloc[0].frameRate,
                                                meta_data=meta
                                               )
    reference.resolve()
    return reference


def rec_path2map_path(rec_path, recMeta, zfill=1):
    return list((rec_path.parent/'maps'/'opendrive').glob(f'{str(recMeta.locationId.values[0]).zfill(zfill)}*/*.xodr'))[0]

@app.command('convert-level-x-data')
def convert_level_x_like(input_path: Path, output_path: Path):
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.mkdir(exist_ok=True, parents=True)
    map_dict = {}
    for t in tqdm(list(input_path.glob('**/*_tracksMeta.csv'))):
        idx = t.stem.split('_')[0]
        pre = t.parent
        recMeta = pd.read_csv(pre/f'{idx}_recordingMeta.csv')
        tracksMeta = pd.read_csv(pre/f'{idx}_tracksMeta.csv')
        tracks = pd.read_csv(pre/f'{idx}_tracks.csv', low_memory=False)
        rec = convert_from_levelx_like(recMeta=recMeta, tracksMeta=tracksMeta, tracks=tracks)
        
        if 'id' in tracks.columns:
            rec.roads = parse_highD_road(recMeta=recMeta, tracks=tracks)
        else:
            try:
                map_path = rec_path2map_path(pre, recMeta, zfill=1)
            except IndexError:
                try:
                    map_path = rec_path2map_path(pre, recMeta, zfill=2)
                except IndexError as e:
                    raise ValueError(f'No Map Data could be found for recording {idx}.') from e
            if map_path not in map_dict:
                map_dict[map_path] = opendrive2roads(map_path).roads_list
            rec.roads = map_dict[map_path]
  
        rec.resolve()
        rec.to_hdf5(output_path/f'{idx}_tracks.hdf5')

        
if __name__ == '__main__':
    app()