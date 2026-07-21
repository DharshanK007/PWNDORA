from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.services.base import CRUDBase

class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    pass

department = CRUDDepartment(Department)
