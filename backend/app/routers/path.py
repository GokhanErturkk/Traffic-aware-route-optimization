from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import database, schemas, models, utils, oauth2
from ..customErrors import CustomError
from ..generateGraph import generate_graph_with_distances
from ..dijikstra import dijkstra_all_paths
from ..pathCameraMapping import CameraPlacements
from sqlalchemy import func
from ..calculate_travel_time import calculate_shortest_path

router = APIRouter(tags=['Authentication'])



@router.post('/car_pass', status_code= status.HTTP_201_CREATED)
def insert_car_pass_data_to_database(carinfo: schemas.CarInfo,db:Session = Depends(get_db)):
    print(carinfo)
    try:
        passing_car = models.CarVelocity(**carinfo.dict())
        db.add(passing_car) 
        db.commit()
        db.refresh(passing_car)

        return {"msg":"Passing car info is inserted to Database successfully."}
    except Exception as e:
        print(e)
        raise CustomError(detail="Something unexpected ocurred.", status_code=500)  


@router.post('/get_fastest_route', status_code= status.HTTP_201_CREATED)
def get_optimum_route(target_node: schemas.TargetNode,db:Session = Depends(get_db)):
    graph = generate_graph_with_distances()

    print(target_node.targetNode)
    start_node = "A" 
    # target_node = "C" # we' ll get this from user
    all_paths = dijkstra_all_paths(graph, start_node, target_node.targetNode)
    print(all_paths)
    
    # we are getting {citypoint: "velocity"..} dict
    try:
         # Subquery to get the max passed_at for each citypoint
        subquery = (
            db.query(
                models.CarVelocity.citypoint,
                func.max(models.CarVelocity.passed_at).label("latest_passed_at")
            )
            .group_by(models.CarVelocity.citypoint)
            .subquery()
        )

        # Join with the main table to get the velocities
        latest_velocities = (
            db.query(
                models.CarVelocity.citypoint,
                models.CarVelocity.velocity
            )
            .join(
                subquery,
                (models.CarVelocity.citypoint == subquery.c.citypoint) &
                (models.CarVelocity.passed_at == subquery.c.latest_passed_at)
            )
            .all()
        )

        # Convert to dictionary format {citypoint: velocity}
        velocity_dict = {record.citypoint: record.velocity for record in latest_velocities}
        
        # Calculate the travel times
        travel_times = calculate_shortest_path(graph, all_paths, velocity_dict, CameraPlacements)

        return {"fastest_path":travel_times}
        # Print the results
        # for travel_time, path in travel_times:
        #     print(f"Path: {path}, Total Travel Time: {travel_time:.2f} units")
        # return {"graph":all_paths}
    
    except Exception as e:
        print(e)
        raise CustomError(detail="Something unexpected ocurred.", status_code=500)  
