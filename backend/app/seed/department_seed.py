from app.models.department import Department

def seed_departments(db):
    dept_names = [
        "Executive Office", "Human Resources", "Engineering", "OT Operations",
        "Production", "Maintenance", "Security Operations", "Procurement",
        "Warehouse", "Finance", "Quality Assurance", "Research & Development"
    ]
    for name in dept_names:
        d = db.query(Department).filter(Department.name == name).first()
        if not d:
            d = Department(name=name, description=f"The {name} department")
            db.add(d)
    db.commit()
    print("Seeded Departments")
