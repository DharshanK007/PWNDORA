from app.models.device import Device, DeviceStatusEnum
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
