from fastapi import APIRouter, Request
from app.database import db_dependency
from app.adapters.employeeAdapter import EmployeeAdapter
from app.models.EmployeeModel import Employee
from app.models.VehicleModel import Vehicle
from app.swagger_models.employeeModels import EmployeeEditRequest, EmployeeRequest

router = APIRouter(prefix="/employee")

@router.get("/all")
def get_all_employee(db: db_dependency, request: Request):
    return EmployeeAdapter().list_all_employees(db, request.query_params)

@router.get("/view/{id:int}")
def get_one_employee(id: int, db: db_dependency):
    return EmployeeAdapter().view_one_employee(id, db)

@router.post("/add")
def create_one_employee(employee: EmployeeRequest, db: db_dependency):
    return EmployeeAdapter().create_one_employee(employee.model_dump(), db)

@router.put("/edit/{id:int}")
def edit_one_employee(id: int, fields: EmployeeEditRequest, db: db_dependency):
    return EmployeeAdapter().edit_one_employee(id, fields, db)

@router.delete("/delete/{id:int}")
def delete_one_employee(id: int, db: db_dependency):
    return EmployeeAdapter().delete_one_employee(id, db)

@router.get("/test")
def test_join(db: db_dependency, request: Request):
    join_test = db.query(Vehicle).join(Employee).all()
    print(join_test[0].brand)
    print(request.query_params)
    return {"data": join_test}