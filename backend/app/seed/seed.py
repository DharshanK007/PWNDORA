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

        # Seed specific Lead Engineer Marcus Chen for Stage 2 FIRST
        marcus_user = User(email="marcus.chen@neofactory.com", hashed_password=default_pwd, role=RoleEnum.ENGINEER)
        db.add(marcus_user)
        db.flush()
        users.append(marcus_user)
        marcus_emp = Employee(
            id="88210345-4242-4111-9999-888888888888",
            user_id=marcus_user.id,
            department_id=departments[0].id,
            first_name="Marcus",
            last_name="Chen",
            phone="+15550192834",
            title="Lead Automation Engineer - Production Line 2",
            clearance_level="Level 4 (OT)"
        )
        db.add(marcus_emp)
        employees.append(marcus_emp)

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
        
        for i in range(198):
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

        # Seed Devices (Line 2 Device FIRST so it's on Page 1)
        devices = []
        line2_dev = Device(
            name="PLC-Line2-FW-Controller",
            mac_address="00:1B:44:11:3A:B7",
            ip_address="192.168.10.42",
            status=DeviceStatusEnum.MAINTENANCE,
            location_id=locations[0].id,
            firmware_id=firmwares[0].id,
            vendor="Vendor PLC Corp",
            asset_group="Production Line 2",
            operating_system="OT-RTOS v1.2.3 (Outdated)",
            maintenance_window="Deferred update — vendor advisory pending review",
            assigned_engineer_id=marcus_emp.id
        )
        db.add(line2_dev)
        devices.append(line2_dev)

        # Seed HMI Terminal Unit-7734 explicitly for SE Stage 3
        hmi_terminal_7734 = Device(
            name="HMI Terminal Unit-7734",
            mac_address="A1:B2:C3:D4:E5:F6",
            ip_address="192.168.10.150",
            status=DeviceStatusEnum.ONLINE,
            location_id=locations[1].id,
            firmware_id=firmwares[1].id,
            vendor="Vendor HMI Corp",
            asset_group="Production",
            operating_system="OT-RTOS v2.0.1",
            maintenance_window="None"
        )
        db.add(hmi_terminal_7734)
        devices.append(hmi_terminal_7734)

        for i in range(99):
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

        # Seed Scenarios (Pilot: Operation Phantom Firmware)
        phantom_scenario = Scenario(
            id="operation_phantom_firmware",
            title="Operation Phantom Firmware",
            description="A maintenance ticket reports that Production Line 2 stopped after a firmware update. Investigate why.",
            business_context="A routine firmware deployment on Production Line 2 failed. Triage suggests a configuration error.",
            difficulty="Intermediate",
            category="Multi-Vector Attack Chain",
            expected_learning_objectives=["Recognize outdated components", "Exploit IDOR in employee records", "Use injection on global search", "Exploit client trust session flaw"]
        )
        db.add(phantom_scenario)

        # ─────────────────────────────────────────────────────────────────────
        # Seed: Silent Exfiltration — Stage 1 Target Account
        # ─────────────────────────────────────────────────────────────────────
        # Password follows the implied migration pattern: Company@Year!
        # The maintenance ticket hints at the convention without stating it.
        # The helpdesk role is low-privilege (EMPLOYEE) — realistic for Stage 1.
        se_target_pwd = get_password_hash("Nf@2024!")
        se_target_user = User(
            email="jess.okafor@neofactory.com",
            hashed_password=se_target_pwd,
            role=RoleEnum.EMPLOYEE
        )
        db.add(se_target_user)
        db.flush()
        se_target_emp = Employee(
            user_id=se_target_user.id,
            department_id=departments[7].id,  # HR department
            first_name="Jess",
            last_name="Okafor",
            title="IT Helpdesk Support",
            phone="+15550288461",
            clearance_level="None"
        )
        db.add(se_target_emp)
        users.append(se_target_user)
        employees.append(se_target_emp)

        # ─────────────────────────────────────────────────────────────────────
        # Seed: HMI device with backup reference (SE Stage 2 discovery lead-in)
        # The search injection results will reference this device's backup file.
        # ─────────────────────────────────────────────────────────────────────
        hmi_device = Device(
            id="77347734-0000-4000-8000-000000000001",
            name="HMI Terminal Unit-7734",
            mac_address="00:2B:67:CC:4A:F1",
            ip_address="192.168.10.88",
            status=DeviceStatusEnum.ONLINE,
            location_id=locations[1].id,
            firmware_id=firmwares[1].id,
            asset_group="Production",
            vendor="Siemens Industrial",
            operating_system="WinCC v7.5",
            maintenance_window="Scheduled quarterly — next: Q3 2026"
        )
        db.add(hmi_device)
        devices.append(hmi_device)

        # ─────────────────────────────────────────────────────────────────────
        # Seed: Maintenance ticket with IT migration hint (SE Stage 1 clue)
        # Written as a real IT person would write a ticket note — implies pattern,
        # does NOT state the password or the exact convention.
        # ─────────────────────────────────────────────────────────────────────
        it_dept_emp = employees[0]  # Admin employee acts as ticket creator
        migration_ticket = MaintenanceTicket(
            device_id=hmi_device.id,
            assigned_to_id=se_target_emp.id,
            created_by_id=it_dept_emp.id,
            priority=PriorityEnum.LOW,
            status=TicketStatusEnum.CLOSED,
            issue_description=(
                "Bulk account migration from legacy Active Directory to new IdP completed. "
                "Helpdesk and support-tier accounts were provisioned with temporary credentials "
                "following the standard migration convention used across all NeoFactory systems. "
                "Reminder sent to affected users to reset at next login — compliance window closes end of month."
            ),
            resolution_notes=(
                "Migration validated. All accounts accessible. Jess Okafor (IT Helpdesk) confirmed login "
                "on 2026-07-01. Reset reminder acknowledged; ticket closed pending user self-service reset."
            )
        )
        migration_ticket.created_at = fake.date_time_between(start_date='-21d', end_date='-18d')
        db.add(migration_ticket)

        # ─────────────────────────────────────────────────────────────────────
        # Seed: Silent Exfiltration scenario record
        # ─────────────────────────────────────────────────────────────────────
        se_scenario = Scenario(
            id="silent_exfiltration",
            title="Silent Exfiltration",
            description="Finance has flagged unusual outbound data activity. Investigate how employee PII was exported without admin credentials.",
            business_context="Finance has flagged unusual outbound data activity, and a customer complaint suggests employee personal data may have been exposed.",
            difficulty="Intermediate",
            category="Multi-Vector Attack Chain",
            expected_learning_objectives=[
                "Exploit missing rate-limiting via credential brute-force",
                "Use injection to leak out-of-scope configuration data",
                "Exploit path traversal to exfiltrate internal service credentials",
                "Leverage stolen credentials to bypass authorization on a privileged endpoint"
            ]
        )
        db.add(se_scenario)

        db.commit()

        # ─────────────────────────────────────────────────────────────────────
        # Create backup files directory and normal backup file for SE Stage 3
        # The secret credentials file is written by the Dockerfile at container start.
        # ─────────────────────────────────────────────────────────────────────
        import os
        backups_dir = "/app/backups"
        os.makedirs(backups_dir, exist_ok=True)
        # Write a normal (non-secret) backup file so the feature feels real
        normal_backup_path = os.path.join(backups_dir, "ot-ctrl-backup-line7.cfg")
        if not os.path.exists(normal_backup_path):
            with open(normal_backup_path, "w") as f:
                f.write("# OT Controller Backup — HMI Terminal Unit-7734\n")
                f.write("# Generated: 2026-07-01T03:00:00Z\n")
                f.write("# Device: HMI Terminal Unit-7734\n")
                f.write("controller_mode=ACTIVE\n")
                f.write("comm_protocol=PROFINET\n")
                f.write("failsafe_timeout=30s\n")
                f.write("watchdog_enabled=true\n")

        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
