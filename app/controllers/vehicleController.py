from fastapi import APIRouter
from app.database import db_dependency
from app.adapters.vehicleAdapter import VehicleAdapter
from app.swagger_models.vehicleModels import VehicleEditRequest, VehicleRequest

router = APIRouter(prefix="/vehicle")

@router.get("/all")
def get_all_vehicles(db: db_dependency):
    return VehicleAdapter().list_all_vehicles(db)

@router.get("/view/{id:int}")
def get_one_vehicle(id: int, db: db_dependency):
    return VehicleAdapter().view_one_vehicle(id, db)

@router.post("/add")
def create_one_vehicle(vehicle: VehicleRequest, db: db_dependency):
    return VehicleAdapter().create_one_vehicle(vehicle.model_dump(), db)

@router.put("/edit/{id:int}")
def edit_one_vehicle(id: int, fields: VehicleEditRequest, db: db_dependency):
    return VehicleAdapter().edit_one_vehicle(id, fields, db)

@router.delete("/delete/{id:int}")
def delete_one_vehicle(id: int, db: db_dependency):
    return VehicleAdapter().delete_one_vehicle(id, db)