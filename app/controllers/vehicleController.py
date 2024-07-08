from fastapi import APIRouter
from app.database import db_dependency
from app.adapters.vehicleAdapter import VehicleAdapter
from app.swagger_models.vehicleModels import VehicleEditRequest, VehicleRequest

router = APIRouter(prefix="/vehicle")

@router.get("/all")
def get_all_vehicles(db: db_dependency):
    return VehicleAdapter().list_all_vehicles()

@router.get("/view/{id:int}")
def get_one_vehicle(id: int, db: db_dependency):
    return VehicleAdapter().view_one_vehicle(id)

@router.post("/add")
def create_one_vehicle(vehicle: VehicleRequest, db: db_dependency):
    return VehicleAdapter().create_one_vehicle(vehicle)

@router.put("/edit/{id:int}")
def edit_one_vehicle(id: int, fields: VehicleEditRequest, db: db_dependency):
    return VehicleAdapter().edit_one_vehicle(id, fields)

@router.delete("/delete/{id:int}")
def delete_one_vehicle(id: int, db: db_dependency):
    return VehicleAdapter().delete_one_vehicle(id)