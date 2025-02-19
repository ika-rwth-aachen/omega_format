def test_create_omega():
    
    import numpy as np
    import omega_format
    from datetime import datetime

    rr = omega_format.ReferenceRecording(meta_data=omega_format.MetaData(recorder_number="1",
                                                                        recording_number="1",
                                                                        daytime=datetime.now(),
                                                                        reference_point_lat=50.786687,
                                                                        reference_point_lon=6.046312),
                                        timestamps=np.array([0]))
    rr.road_users[0] = omega_format.RoadUser(type=omega_format.ReferenceTypes.RoadUserType.CAR,
                                            subtype=omega_format.ReferenceTypes.RoadUserSubTypeGeneral.REGULAR,
                                            birth=0,
                                            bb=omega_format.BoundingBox(vec=np.array([2,3,1])),
                                            tr=omega_format.Trajectory(pos_x=np.array([0]),
                                                                        pos_y=np.array([0]),
                                                                        pos_z=np.array([0]),
                                                                        heading=np.array([0]),
                                                                        vel_longitudinal=np.array([0]),
                                                                        vel_lateral=np.array([0]),
                                                                        vel_z=np.array([0]),
                                                                        acc_longitudinal=np.array([0]),
                                                                        acc_lateral=np.array([0]),
                                                                        acc_z=np.array([0]),
                                                                        roll_der=np.array([0]),
                                                                        pitch_der=np.array([0]),
                                                                        heading_der=np.array([0]),
                                                                        pitch=np.array([0]),
                                                                        roll=np.array([0])))
    rr.roads[0] = omega_format.Road(location=omega_format.ReferenceTypes.RoadLocation.URBAN)
    rr.to_hdf5('test.hdf5')
    
def test_read_created_file():
    import omega_format
    
    omega_format.ReferenceRecording.from_hdf5('test.hdf5')
    
    
def test_part_create_omega():
    
    import numpy as np
    import omega_format
    from datetime import datetime

    rr = omega_format.ReferenceRecording(meta_data=omega_format.MetaData(recorder_number="1",
                                                                        recording_number="1",
                                                                        daytime=datetime.now(),
                                                                        reference_point_lat=50.786687,
                                                                        reference_point_lon=6.046312),
                                        timestamps=np.array([0]))
    rr.road_users[0] = omega_format.RoadUser(type=omega_format.ReferenceTypes.RoadUserType.CAR,
                                            birth=0,
                                            bb=omega_format.BoundingBox(vec=np.array([2,3,1])),
                                            tr=omega_format.Trajectory(pos_x=np.array([0]),
                                                                        pos_y=np.array([0]),
                                                                        pos_z=np.array([0]),
                                                                        heading=np.array([0])))
    rr.roads[0] = omega_format.Road(location=omega_format.ReferenceTypes.RoadLocation.URBAN)
    rr.to_hdf5('test_partly.hdf5')
    
def test_part_read_created_file():
    import omega_format
    
    omega_format.ReferenceRecording.from_hdf5('test_partly.hdf5')