import os

base = "backend/app/seed"
os.makedirs(base, exist_ok=True)

# utils.py
with open(os.path.join(base, "utils.py"), "w") as f:
    f.write('''import os
import sys
from faker import Faker
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

fake = Faker()

def get_random_enum_value(enum_class):
    return random.choice(list(enum_class))
''')

# company_seed.py
with open(os.path.join(base, "company_seed.py"), "w") as f:
    f.write('''from app.models.company import CompanyProfile

def seed_company(db):
    company = db.query(CompanyProfile).first()
    if not company:
        company = CompanyProfile(
            name="NeoFactory Industries",
            description="Leading manufacturer of smart industrial components.",
            headquarters="Detroit, MI, USA",
            business_units=["Automotive", "Aerospace", "Consumer Electronics"],
            industry="Manufacturing",
            employee_count=15000,
            contact_email="contact@neofactory.com",
            business_domain="Industrial Automation",
            security_level="Tier-2 Enterprise",
            factory_count=5,
            office_count=12,
            critical_infrastructure_type="Smart Factory",
            timezone="UTC-5"
        )
        db.add(company)
        db.commit()
    print("Seeded Company Profile")
''')

# department_seed.py
with open(os.path.join(base, "department_seed.py"), "w") as f:
    f.write('''from app.models.department import Department

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
''')

# network_seed.py
with open(os.path.join(base, "network_seed.py"), "w") as f:
    f.write('''from app.models.network import NetworkZone, NetworkLink

def seed_networks(db):
    zone_names = ["Corporate LAN", "DMZ", "Factory LAN", "OT Network", "ICS Zone", "PLC Network", "VPN"]
    zones = {}
    for idx, name in enumerate(zone_names):
        z = db.query(NetworkZone).filter(NetworkZone.name == name).first()
        if not z:
            z = NetworkZone(name=name, vlan_id=10+idx, subnet=f"10.0.{idx}.0/24", trust_level="Medium", routing_direction="Bi-directional")
            db.add(z)
            db.flush()
        zones[name] = z
    db.commit()
    
    # Create links if not exist
    if db.query(NetworkLink).count() == 0:
        links = [
            ("Corporate LAN", "DMZ"),
            ("DMZ", "Factory LAN"),
            ("Factory LAN", "OT Network"),
            ("OT Network", "ICS Zone"),
            ("ICS Zone", "PLC Network")
        ]
        for src, dst in links:
            if src in zones and dst in zones:
                link = NetworkLink(
                    source_zone_id=zones[src].id,
                    target_zone_id=zones[dst].id,
                    description=f"Route from {src} to {dst}"
                )
                db.add(link)
        db.commit()
    print("Seeded Network Zones and Links")
''')

# employee_seed.py
with open(os.path.join(base, "employee_seed.py"), "w") as f:
    f.write('''from app.models.employee import Employee, EmployeeStatusEnum
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
''')

# device_seed.py
with open(os.path.join(base, "device_seed.py"), "w") as f:
    f.write('''from app.models.device import Device, DeviceStatusEnum
from app.models.network import NetworkZone
from app.models.employee import Employee
from app.seed.utils import fake
import random

def seed_devices(db):
    if db.query(Device).count() >= 100:
        print("Devices already seeded")
        return
        
    zones = db.query(NetworkZone).all()
    employees = db.query(Employee).all()
    if not zones or not employees: return
    
    manufacturers = ["Siemens", "Allen-Bradley", "Rockwell", "ABB", "Schneider Electric"]
    protocols = ["Modbus", "OPC-UA", "EtherNet/IP", "PROFINET", "MQTT"]
    
    print("Generating 100 Industrial Devices...")
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
            network_zone_id=random.choice(zones).id,
            criticality_level=random.choice(["High", "Medium", "Low"]),
            operating_system=random.choice(["VxWorks", "Linux", "Windows CE", "Embedded RTOS"]),
            last_patch_date=str(fake.date_this_year()),
            maintenance_window="Saturday 02:00 AM",
            communication_protocol=random.choice(protocols),
            vendor=random.choice(manufacturers),
            asset_group=random.choice(["Assembly", "Packaging", "Quality Control", "HVAC"])
        )
        db.add(d)
    db.commit()
    print("Seeded 100 Devices")
''')

# firmware_seed.py
with open(os.path.join(base, "firmware_seed.py"), "w") as f:
    f.write('''def seed_firmware(db):
    print("Seeded Firmware (Stub)")
''')

# maintenance_seed.py
with open(os.path.join(base, "maintenance_seed.py"), "w") as f:
    f.write('''from app.models.maintenance_ticket import MaintenanceTicket, TicketStatusEnum
from app.models.device import Device
from app.models.employee import Employee
from app.seed.utils import fake
import random

def seed_maintenance(db):
    if db.query(MaintenanceTicket).count() >= 50:
        return
        
    devices = db.query(Device).all()
    employees = db.query(Employee).all()
    if not employees: return
    
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
''')

# inventory_seed.py
with open(os.path.join(base, "inventory_seed.py"), "w") as f:
    f.write('''def seed_inventory(db):
    print("Seeded Inventory (Stub)")
''')

# notification_seed.py
with open(os.path.join(base, "notification_seed.py"), "w") as f:
    f.write('''def seed_notifications(db):
    print("Seeded Notifications (Stub)")
''')

# activity_seed.py
with open(os.path.join(base, "activity_seed.py"), "w") as f:
    f.write('''def seed_activity(db):
    print("Seeded Activity Logs (Stub)")
''')

# scenario_seed.py
with open(os.path.join(base, "scenario_seed.py"), "w") as f:
    f.write('''from app.scenarios.scenario_model import Scenario
from app.models.department import Department
import random

def seed_scenarios(db):
    if db.query(Scenario).count() > 0:
        return
        
    depts = db.query(Department).all()
    dept_id = depts[0].id if depts else None
    
    scenarios = [
        Scenario(
            title="Ransomware on Factory LAN",
            description="Simulated lateral movement from corporate network into the OT environment.",
            business_context="Production line 3 halted due to suspected infection.",
            difficulty="Advanced",
            category="Incident Response",
            expected_learning_objectives=["Identify lateral movement", "Isolate OT network", "Analyze PCAP"],
            scenario_type="Tabletop",
            business_impact="Critical",
            target_department_id=dept_id,
            estimated_duration="2 hours",
            required_roles=["SOC Analyst", "OT Engineer"],
            tags=["Ransomware", "Lateral Movement"]
        ),
        Scenario(
            title="Rogue PLC Firmware Update",
            description="An unauthorized firmware update was pushed to the main PLC.",
            business_context="Quality control detected anomalies in physical outputs.",
            difficulty="Intermediate",
            category="Forensics",
            expected_learning_objectives=["Verify firmware signatures", "Check audit logs", "Restore known-good state"],
            scenario_type="Live Fire",
            business_impact="High",
            target_department_id=dept_id,
            estimated_duration="4 hours",
            required_roles=["ICS Security Specialist"],
            tags=["PLC", "Firmware", "Unauthorized Access"]
        )
    ]
    db.bulk_save_objects(scenarios)
    db.commit()
    print("Seeded Scenarios")
''')

# master_seed.py
with open(os.path.join(base, "master_seed.py"), "w") as f:
    f.write('''import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.session import SessionLocal
from app.seed.company_seed import seed_company
from app.seed.department_seed import seed_departments
from app.seed.network_seed import seed_networks
from app.seed.employee_seed import seed_employees
from app.seed.device_seed import seed_devices
from app.seed.firmware_seed import seed_firmware
from app.seed.maintenance_seed import seed_maintenance
from app.seed.inventory_seed import seed_inventory
from app.seed.notification_seed import seed_notifications
from app.seed.activity_seed import seed_activity
from app.seed.scenario_seed import seed_scenarios
from app.db.base_class import Base
from app.db.session import engine

def run_all():
    db = SessionLocal()
    
    # We should clean DB to avoid conflicts when seeding afresh
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    print("Starting Modular Enterprise Data Generation (Milestone 3D)...")
    seed_company(db)
    seed_departments(db)
    seed_networks(db)
    seed_employees(db)
    seed_devices(db)
    seed_firmware(db)
    seed_maintenance(db)
    seed_inventory(db)
    seed_notifications(db)
    seed_activity(db)
    seed_scenarios(db)
    print("Enterprise Seeding Complete.")

if __name__ == "__main__":
    run_all()
''')

print("Created modular seed engine")
