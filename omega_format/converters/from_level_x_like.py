import pandas as pd
from pathlib import Path
import omega_format
import numpy as np
from tqdm.auto import tqdm
from omega_format import DictWithProperties, ReferenceElement
from datetime import datetime
import warnings
import typer
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = typer.Typer()

bound_solid = omega_format.enums.reference_types.BoundaryType.SOLID
bound_dashed = omega_format.enums.reference_types.BoundaryType.DASHED


def parse_highD_road(recMeta_path, tracks_path):
    recMeta = pd.read_csv(recMeta_path)
    tracks = pd.read_csv(tracks_path)
    
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
                sub_type=omega_format.enums.reference_types.LaneSubType.UNKNOWN,
                classification=omega_format.enums.reference_types.LaneClass.NONE,
                border_right_is_inverted=direction=='lowerLaneMarkings',
                border_left_is_inverted=direction=='lowerLaneMarkings',
                boundaries=DictWithProperties({0: omega_format.Boundary(poly_index_start=0, poly_index_end=3, is_right_boundary=True,
                                                                        color=omega_format.enums.reference_types.BoundaryColor.WHITE,
                                                                        condition=omega_format.enums.reference_types.BoundaryCondition.FINE,
                                                                        type=bound_dashed if right_border_id not in [border_ids[0],border_ids[-1]] else bound_solid,
                                                                        sub_type=omega_format.enums.reference_types.BoundarySubType.THICK,), 
                                               1: omega_format.Boundary(poly_index_start=0, poly_index_end=3, is_right_boundary=False,
                                                                        color=omega_format.enums.reference_types.BoundaryColor.WHITE,
                                                                        condition=omega_format.enums.reference_types.BoundaryCondition.FINE,
                                                                        type=bound_dashed if left_border_id not in [border_ids[0],border_ids[-1]] else bound_solid,
                                                                        sub_type=omega_format.enums.reference_types.BoundarySubType.THICK,)})
            )
        roads[rid] = omega_format.Road(
            lanes=lanes,
            borders=borders,
            location=omega_format.enums.reference_types.RoadLocation.HIGHWAY
        )
    return roads

@app.command('levelxobjects')
def convert_from_levelx_like(recMeta_path: Path, tracksMeta_path: Path, tracks_path: Path):
    recMeta = pd.read_csv(recMeta_path)
    tracksMeta = pd.read_csv(tracksMeta_path)
    tracks = pd.read_csv(tracks_path)
   
        
    ru = omega_format.enums.reference_types
    type_mapping = {
        'Car': ru.RoadUserType.CAR,
        'Truck': ru.RoadUserType.TRUCK
    }

    road_users = DictWithProperties()
    for idx, (_, road_user) in tqdm(list(enumerate(tracksMeta.iterrows())),leave=False):
        track_of_road_user = tracks[tracks.id==road_user.id]
        tr = omega_format.dynamics.trajectory.Trajectory(
            pos_x=(track_of_road_user['x']+track_of_road_user['width']/2).to_numpy(),
            pos_y=(track_of_road_user['y']+track_of_road_user['height']/2).to_numpy(),
            pos_z=np.zeros(len(track_of_road_user)),
            heading=180*np.ones(len(track_of_road_user))*(road_user.drivingDirection==1),
            vel_longitudinal=track_of_road_user['xVelocity'].to_numpy(),
            vel_lateral=track_of_road_user['yVelocity'].to_numpy(),
            acc_longitudinal=track_of_road_user['xAcceleration'].to_numpy(),
            acc_lateral=track_of_road_user['yAcceleration'].to_numpy()
        )
        bb = np.ones(3)
        bb[:2] = road_user[['width','height']].to_numpy() #(length, widht, height)
        bb = omega_format.dynamics.bounding_box.BoundingBox(vec=bb)
        road_users[f'RU({road_user.id})'] = omega_format.RoadUser(bb=bb, tr=tr, birth=road_user.initialFrame , sub_type=ru.RoadUserSubTypeGeneral.REGULAR, type=type_mapping[road_user['class']], connected_to=ReferenceElement(-1, omega_format.RoadUser))
    start_time= datetime.strptime(str(recMeta.iloc[0].startTime) + ' ' + str(recMeta.iloc[0].month) + ' ' + str(recMeta.iloc[0].weekDay), '%H:%M %m.%Y %a')
    meta = omega_format.MetaData(daytime=start_time,
                                recorder_number="ika",
                                recording_number=str(recMeta.iloc[0].id),
                                reference_point_lat=0,
                                reference_point_lon=0,
                                reference_modality=3,
                                natural_behavior=True,
                                natural_exposure=True,)
    reference = omega_format.ReferenceRecording(road_users=road_users,
                                                timestamps=omega_format.Timestamps(val=tracks.frame.unique()/recMeta.iloc[0].frameRate),
                                                meta_data=meta
                                               )
    reference.resolve()
    return reference


@app.command('folder')
def convert_highD_like_folder(input_path: Path, output_path: Path):
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.mkdir(exist_ok=True)
    for t in tqdm(list(input_path.glob('**/*_tracksMeta.csv'))):
        idx = t.stem.split('_')[0]
        pre = t.parent
        rec = convert_from_levelx_like(recMeta_path=pre/f'{idx}_recordingMeta.csv',tracksMeta_path=pre/f'{idx}_tracksMeta.csv',tracks_path=pre/f'{idx}_tracks.csv')
        rec.roads = parse_highD_road(recMeta_path=pre/f'{idx}_recordingMeta.csv', tracks_path=pre/f'{idx}_tracks.csv')
        rec.resolve()
        rec.to_hdf5(output_path/f'{idx}_tracks.hdf5')

        
if __name__ == '__main__':
    convert_highD_like_folder('../../../../datasets/highd-dataset-v1.0/', './test')
