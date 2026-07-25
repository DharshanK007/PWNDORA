import os
os.makedirs("backend/app/seed", exist_ok=True)

seed_code = '''import os
import sys
from faker import Faker
import random
from uuid import uuid4
import datetime

# Setup paths for script execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.session import SessionLocal
from app.models.company import CompanyProfile
from app.models.department import Department
from app.models.network import NetworkZone
from app.models.user import User
from app.models.employee import Employee, EmployeeStatusEnum
from app.models.device import Device, DeviceStatusEnum
from app.models.maintenance_ticket import MaintenanceTicket, TicketStatusEnum
from app.scenarios.scenario_model import Scenario
from app.core.security import get_password_hash

fake = Faker()

def seed_database():
    db = SessionLocal()
    print("Starting Enterprise Data Generation (Milestone 3D)...")

    # 1. Company Profile
    company = db.query(CompanyProfile).first()
    if not company:
        company = CompanyProfile(
            name="NeoFactory Industries",
            description="Leading manufacturer of smart industrial components.",
            headquarters="Detroit, MI, USA",
            business_units=["Automotive", "Aerospace", "Consumer Electronics"],
            industry="Manufacturing",
            employee_count=15000,
            contact_email="contact@neofactory.com"
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        print("Seeded Company Profile")

    # 2. Departments
    dept_names = [
        "Executive Office", "Human Resources", "Engineering", "OT Operations",
        "Production", "Maintenance", "Security Operations", "Procurement",
        "Warehouse", "Finance", "Quality Assurance", "Research & Development"
    ]
    depts = []
    for name in dept_names:
        d = db.query(Department).filter(Department.name == name).first()
        if not d:
            d = Department(name=name, description=f"The {name} department")
            db.add(d)
        depts.append(d)
    db.commit()
    print("Seeded Departments")

    # 3. Network Zones
    zone_names = ["Corporate LAN", "Factory LAN", "OT Network", "ICS Zone", "DMZ", "VPN"]
    zones = []
    for idx, name in enumerate(zone_names):
        z = db.query(NetworkZone).filter(NetworkZone.name == name).first()
        if not z:
            z = NetworkZone(name=name, vlan_id=10+idx, subnet=f"10.0.{idx}.0/24")
            db.add(z)
        zones.append(z)
    db.commit()
    print("Seeded Network Zones")

    # 4. Users & Employees
    # Generate 200 Employees
    existing_emps = db.query(Employee).count()
    if existing_emps < 200:
        print("Generating 200 Employees. This may take a moment...")
        # Create CEO first
        ceo_user = User(email="ceo@neofactory.com", hashed_password=get_password_hash("password123"), role="Admin")
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
            shift="Day"
        )
        db.add(ceo)
        db.flush()
        
        employees = [ceo]
        
        roles = ["Manager", "Lead Engineer", "Engineer", "Operator", "Technician"]
        
        for i in range(200):
            u = User(
                email=fake.unique.email(),
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
                manager_id=random.choice(employees).id if i > 5 else ceo.id
            )
            db.add(e)
            employees.append(e)
        
        db.commit()
        print("Seeded 200 Employees")

    employees = db.query(Employee).all()

    # 5. Devices
    existing_devs = db.query(Device).count()
    if existing_devs < 100:
        print("Generating 100 Industrial Devices...")
        manufacturers = ["Siemens", "Allen-Bradley", "Rockwell", "ABB", "Schneider Electric"]
        for i in range(100):
            d = Device(
                name=f"Device-{i}",
                mac_address=fake.unique.mac_address(),
                ip_address=fake.ipv4(),
                status=random.choice(list(DeviceStatusEnum)),
                serial_number=fake.uuid4()[:10],
                manufacturer=random.choice(manufacturers),
                lifecycle_status=random.choice(["Active", "Active", "EOL"]),
                assigned_engineer_id=random.choice(employees).id,
                network_zone_id=random.choice(zones).id
            )
            db.add(d)
        db.commit()
        print("Seeded 100 Devices")
        
    devices = db.query(Device).all()

    # 6. Scenarios
    existing_scenarios = db.query(Scenario).count()
    if existing_scenarios == 0:
        scenarios = [
            Scenario(
                title="Ransomware on Factory LAN",
                description="Simulated lateral movement from corporate network into the OT environment.",
                business_context="Production line 3 halted due to suspected infection.",
                difficulty="Advanced",
                category="Incident Response",
                expected_learning_objectives=["Identify lateral movement", "Isolate OT network", "Analyze PCAP"]
            ),
            Scenario(
                title="Rogue PLC Firmware Update",
                description="An unauthorized firmware update was pushed to the main PLC.",
                business_context="Quality control detected anomalies in physical outputs.",
                difficulty="Intermediate",
                category="Forensics",
                expected_learning_objectives=["Verify firmware signatures", "Check audit logs", "Restore known-good state"]
            )
        ]
        db.bulk_save_objects(scenarios)
        db.commit()
        print("Seeded Scenarios")

    # 7. Tickets
    existing_tickets = db.query(MaintenanceTicket).count()
    if existing_tickets < 50:
        print("Generating Maintenance Tickets...")
        for i in range(50):
            t = MaintenanceTicket(
                title=f"Maintenance for {fake.word()}",
                description=fake.text(),
                status=random.choice(list(TicketStatusEnum)),
                device_id=random.choice(devices).id if devices else None,
                created_by_id=random.choice(employees).id,
                assigned_to_id=random.choice(employees).id
            )
            db.add(t)
        db.commit()
        print("Seeded Tickets")

    print("Enterprise Seeding Complete.")

if __name__ == "__main__":
    seed_database()
'''
with open("backend/app/seed/engine.py", "w") as f:
    f.write(seed_code)

print("Created seed engine.")
