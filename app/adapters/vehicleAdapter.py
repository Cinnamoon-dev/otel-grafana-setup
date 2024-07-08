import json
from fastapi import Response
from app import instance_update
from sqlalchemy.orm import Session
from app.models.VehicleModel import Vehicle
from app.models.EmployeeModel import Employee
from app.swagger_models.vehicleModels import VehicleRequest, VehicleEditRequest

class VehicleAdapter():
    def list_all_vehicles(self, db: Session):
        vehicles = db.query(Vehicle).all()

        return {"data": [vehicle.relationship_to_dict() for vehicle in vehicles]}

    def view_one_vehicle(self, id: int, db: Session):
        vehicle = db.query(Vehicle).get(id)

        if not vehicle:
            return Response(json.dumps({"error": True, "message": "Vehicle not found"}), 404) 

        return vehicle.to_dict()

    def create_one_vehicle(self, request: dict[VehicleRequest], db: Session):
        if not db.query(Employee).filter(Employee.id == request.get("employee_id")).first():
            return Response(json.dumps({"error": True, "message": "Employee not found"}), 404)

        if db.query(Vehicle).filter(Vehicle.plate == request.get("plate")).first():
            return Response(json.dumps({"error": True, "message": "Plate already exists"}), 409)
        
        newVehicle = Vehicle(**request)
        db.add(newVehicle)

        try:
            db.flush()
            db.commit()
            return Response(json.dumps({"error": False, "message": "Vehicle created successfully"}), 200)
        except:
            db.rollback()
            return Response(json.dumps({"error": True, "message": "Database error"}), 500)

    def edit_one_vehicle(self, id: int, request: dict[VehicleEditRequest], db: Session):
        vehicle = db.query(Vehicle).get(id)

        if not vehicle:
            return Response(json.dumps({"error": True, "message": "Vehicle not found"}), 404)

        instance_update(vehicle, request)

        try:
            db.commit()
            return Response(json.dumps({"error": False, "message": "Vehicle edited successfully"}))
        except:
            db.rollback()
            return Response(json.dumps({"error": True, "message": "Database Error"}, 500))

    def delete_one_vehicle(self, id: int, db: Session):
        vehicle = db.query(Vehicle).get(id)

        if not vehicle:
            return Response(json.dumps({"error": True, "message": "Vehicle not found"}), 404)
        
        try:
            db.delete(vehicle)
            db.flush()
            db.commit()
            return Response(json.dumps({"error": False, "message": "Vehicle deleted successfully"}))
            
        except:
            db.rollback()
            return Response(json.dumps({"error": True, "message": "Database error"}), 500)