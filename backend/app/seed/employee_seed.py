from app.models.employee import Employee, EmployeeStatusEnum
from app.models.user import User
from app.models.department import Department
from app.core.security import get_password_hash
from app.seed.utils import fake
import random

def seed_employees(db):
    existing_emps = db.query(Employee).count()
    if existing_emps >= 200:
        print("Employees already seeded")
        return

    depts = db.query(Department).all()
    if not depts: return
    
    print("Generating 200 Employees. This may take a moment...")
    ceo_user = User(email="ceo@neofactory.com", hashed_password=get_password_hash("password123"), role="Administrator")
    db.add(ceo_user)
    db.flush()
    ceo = Employee(
        user_id=ceo_user.id,
        department_id=depts[0].id,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        title="CEO",
        status=EmployeeStatusEnum.ACTIVE,
        office="HQ 1A",
        shift="Day",
        role_level="Executive",
        hire_date=str(fake.date_between(start_date='-10y', end_date='today')),
        last_login=str(fake.date_time_this_month()),
        badge_id=fake.uuid4()[:8],
        clearance_level="Top Secret",
        employment_type="Full-time",
        workstation="HQ-WS-01",
        assigned_projects=["Strategic Plan 2030"],
        security_training_completed=True
    )
    db.add(ceo)
    db.flush()
    
    employees = [ceo]
    roles = ["Manager", "Lead Engineer", "Engineer", "Operator", "Technician"]
    levels = ["Management", "Engineering", "Operations", "Support", "External Vendor", "Contractor"]
    
    users = []
    emps = []
    
    for i in range(200):
        email = fake.unique.email()
        u = User(
            email=email,
            hashed_password=get_password_hash("password123"),
            role="Employee"
        )
        db.add(u)
        db.flush()
        
        e = Employee(
            user_id=u.id,
            department_id=random.choice(depts).id,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            title=random.choice(roles),
            status=EmployeeStatusEnum.ACTIVE,
            office=f"Building {random.randint(1,5)}",
            shift=random.choice(["Day", "Night", "Swing"]),
            skills=[fake.job() for _ in range(3)],
            manager_id=random.choice(employees).id if i > 5 else ceo.id,
            role_level=random.choice(levels),
            hire_date=str(fake.date_between(start_date='-5y', end_date='today')),
            last_login=str(fake.date_time_this_month()),
            badge_id=fake.uuid4()[:8],
            clearance_level=random.choice(["Secret", "Confidential", "None"]),
            employment_type=random.choice(["Full-time", "Contractor", "Part-time"]),
            workstation=f"WS-{fake.uuid4()[:4]}",
            assigned_projects=[fake.bs()],
            security_training_completed=random.choice([True, False])
        )
        db.add(e)
        employees.append(e)
    
    db.commit()
    print("Seeded 200 Employees")
