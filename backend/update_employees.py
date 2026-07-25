import os
import random
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User, RoleEnum
from app.models.employee import Employee, EmployeeStatusEnum
from app.models.department import Department
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
default_pwd = pwd_context.hash("neosecurepass")

SQLALCHEMY_DATABASE_URI = "postgresql://neofactory:neosecurepass@postgres:5432/neofactory"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run():
    db = SessionLocal()
    
    employees = db.query(Employee).all()
    
    lines = [f"Production Line {i}" for i in range(1, 8)]
    clearances = ["OT", "Analyst", "HR", "Dev", "Assoc", "R&D dep"]
    
    target_total = 420
    current_count = len(employees)
    to_create = max(0, target_total - current_count)
    
    department = db.query(Department).first()
    
    for i in range(to_create):
        uid = str(uuid.uuid4())
        email = f"emp{i}_{uid[:8]}@neofactory.com"
        user = User(id=uid, email=email, hashed_password=default_pwd, role=RoleEnum.EMPLOYEE)
        db.add(user)
        
        emp = Employee(
            id=str(uuid.uuid4()),
            user_id=uid,
            department_id=department.id,
            first_name=f"User{i}",
            last_name=f"Test{i}",
            status=EmployeeStatusEnum.ACTIVE,
            title="Worker",
            clearance_level="OT"
        )
        db.add(emp)
        
    db.commit()
    
    all_emps = db.query(Employee).all()
    
    line_assignments = []
    for i in range(7):
        line_assignments.extend([lines[i]] * 60)
        
    while len(line_assignments) < len(all_emps):
        line_assignments.append(random.choice(lines))
        
    random.shuffle(line_assignments)
    
    for idx, emp in enumerate(all_emps):
        old_title = emp.title or "Engineer"
        
        if emp.id == "88210345-4242-4111-9999-888888888888":
            new_line = "Production Line 2"
            new_clearance = "OT"
            base_title = "Lead Automation Engineer"
            new_title = f"{base_title} - {new_line}"
        else:
            new_line = line_assignments[idx]
            new_clearance = random.choice(clearances)
            base_title = old_title.split(" - Production")[0]
            if base_title == "Worker":
                base_title = random.choice(["Technician", "Operator", "Supervisor", "Engineer"])
            new_title = f"{base_title} - {new_line}"
            
        emp.title = new_title
        emp.clearance_level = new_clearance
        
    db.commit()
    print(f"Updated {len(all_emps)} employees.")
    
if __name__ == '__main__':
    run()
