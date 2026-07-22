import os
import sys
import random
from datetime import datetime, timedelta, timezone
from faker import Faker
from uuid import uuid4

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.core.security import get_password_hash
from app.models import (
    User, RoleEnum, Department, Employee, MachineLocation, Firmware,
    Device, DeviceStatusEnum, MaintenanceTicket, PriorityEnum, TicketStatusEnum,
    Inventory, Report, Notification, ActivityLog
)
from app.scenarios.scenario_model import Scenario

fake = Faker()

def seed_db():
    print("Starting database seed...")
    # Drop and recreate all tables for a clean slate during dev
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Seed Departments
        departments = []
        dept_names = ["OT Operations", "R&D", "Logistics", "Cyber Security", "Production", "Maintenance", "Inventory", "HR", "Finance", "Quality Assurance"]
        for name in dept_names:
            dept = Department(name=name, description=fake.catch_phrase())
            db.add(dept)
            departments.append(dept)
        db.commit()

        # Seed Users and Employees (50 total)
        users = []
        employees = []
        default_pwd = get_password_hash("password123")
        
        # Add 1 admin
        admin_user = User(email="ceo@neofactory.com", hashed_password=default_pwd, role=RoleEnum.ADMINISTRATOR)
        db.add(admin_user)
        db.flush()
        users.append(admin_user)
        admin_emp = Employee(user_id=admin_user.id, department_id=departments[0].id, first_name="System", last_name="Admin", phone=f"+1{fake.numerify('##########')}")
        db.add(admin_emp)
        employees.append(admin_emp)

        roles = [RoleEnum.EMPLOYEE, RoleEnum.ENGINEER, RoleEnum.MANAGER]
        job_titles = [
            "Senior Automation Engineer", "SCADA Administrator", "OT Security Analyst",
            "Plant Manager", "Chief Information Security Officer", "VP of Operations",
            "Reliability Engineer", "Controls Engineer", "Industrial Network Specialist",
            "Maintenance Supervisor", "Production Coordinator", "Quality Assurance Director",
            "Robotics Technician", "ICS Incident Responder", "Compliance Officer",
            "Systems Integrator", "Data Scientist", "Lead Field Technician",
            "Shift Supervisor", "Process Control Engineer", "Director of Manufacturing"
        ]
        
        for i in range(199):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}{i}@neofactory.com"
            user = User(email=email, hashed_password=default_pwd, role=random.choice(roles))
            db.add(user)
            db.flush()
            users.append(user)
            
            emp = Employee(
                user_id=user.id,
                department_id=random.choice(departments).id,
                first_name=first_name,
                last_name=last_name,
                phone=f"+1{fake.numerify('##########')}",
                title=random.choice(job_titles),
                clearance_level=random.choice(["None", "Confidential", "Secret", "Top Secret", "Level 4 (OT)"])
            )
            db.add(emp)
            employees.append(emp)
        db.commit()

        # Seed MachineLocations
        locations = []
        zones = ["Line A", "Line B", "Clean Room", "Warehouse", "Loading Dock"]
        for i in range(10):
            loc = MachineLocation(factory_site=fake.city(), zone=random.choice(zones), description=fake.sentence())
            db.add(loc)
            locations.append(loc)
        db.commit()

        # Seed Firmware (50)
        firmwares = []
        for i in range(50):
            fw = Firmware(
                version_string=f"v{random.randint(1,5)}.{random.randint(0,9)}.{i}",
                release_date=fake.date_between(start_date='-2y', end_date='today'),
                file_hash=fake.sha256(),
                s3_path=f"s3://neofactory-firmware/{fake.uuid4()}.bin",
                compatibility_matrix="Universal",
                is_active=random.choice([True, False])
            )
            db.add(fw)
            firmwares.append(fw)
        db.commit()

        # Seed Devices (100)
        devices = []
        for i in range(100):
            is_network = i < 15  # Make the first 15 devices network infrastructure
            
            if is_network:
                names = ["Core Switch", "Distribution Switch", "Edge Router", "Access Switch", "Core Firewall", "VPN Gateway", "DMZ Switch"]
                dev_name = f"{random.choice(names)} {random.randint(10,99)}"
                asset_group = "Network"
            else:
                names = ["PLC", "HMI Panel", "Robotic Arm", "Conveyor Sensor", "HVAC Controller", "CNC Machine", "SCADA Server"]
                dev_name = f"{random.choice(names)} Unit-{random.randint(1000,9999)}"
                asset_group = random.choice(["Production", "HVAC", "Safety", "Control Systems"])

            dev = Device(
                name=dev_name,
                mac_address=fake.mac_address(),
                ip_address=fake.ipv4_private(),
                status=random.choice(list(DeviceStatusEnum)),
                location_id=random.choice(locations).id,
                firmware_id=random.choice(firmwares).id,
                asset_group=asset_group
            )
            db.add(dev)
            devices.append(dev)
        db.commit()

        # Seed Maintenance Tickets (200)
        for i in range(200):
            ticket = MaintenanceTicket(
                device_id=random.choice(devices).id,
                assigned_to_id=random.choice(employees).id if random.random() > 0.2 else None,
                created_by_id=random.choice(employees).id,
                priority=random.choice(list(PriorityEnum)),
                status=random.choice(list(TicketStatusEnum)),
                issue_description=fake.paragraph(),
                resolution_notes=fake.paragraph() if random.random() > 0.5 else None
            )
            ticket.created_at = fake.date_time_between(start_date='-1y', end_date='now')
            db.add(ticket)
        
        # Seed Inventory (100)
        for i in range(100):
            inv = Inventory(
                component_name=fake.catch_phrase(),
                part_number=f"PN-{fake.ean(length=8)}",
                stock_quantity=random.randint(0, 500),
                warehouse_zone=random.choice(["A", "B", "C", "D"]),
                supplier=fake.company()
            )
            db.add(inv)

        # Seed Reports (20)
        # for i in range(20):
        #     rep = Report(
        #         title=f"Monthly {fake.word()} Report",
        #         report_type=random.choice(["Production", "Maintenance", "Inventory"]),
        #         file_path=f"/reports/{fake.uuid4()}.pdf",
        #         summary=fake.paragraph(),
        #         generated_by_id=random.choice(employees).id
        #     )
        #     db.add(rep)

        # Seed Notifications (30)
        for i in range(30):
            notif = Notification(
                recipient_id=random.choice(users).id,
                title=fake.sentence(nb_words=4),
                message=fake.paragraph(),
                read_status=random.choice([True, False]),
                severity=random.choice(["INFO", "WARNING", "ERROR"])
            )
            db.add(notif)

        # Seed Activity Logs (500)
        for i in range(500):
            log = ActivityLog(
                user_id=random.choice(users).id if random.random() > 0.1 else None,
                action=random.choice(["LOGIN", "UPDATE_FIRMWARE", "CREATE_TICKET", "DOWNLOAD_REPORT"]),
                target_entity=fake.word(),
                ip_address=fake.ipv4_private()
            )
            log.created_at = fake.date_time_between(start_date='-30d', end_date='now')
        # Seed Scenarios
        scenario_1 = Scenario(
            id="scenario_001",
            title="Operation Phantom Firmware",
            description="A routine firmware deployment on Production Line 2 failed...",
            business_context="Initial triage suggests a configuration error...",
            difficulty="Intermediate",
            category="Multi-Vector Attack Chain",
            expected_learning_objectives=["Identify authorization flaws", "Find leaked credentials"]
        )
        db.add(scenario_1)

        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
