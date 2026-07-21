from app.models.maintenance_ticket import MaintenanceTicket, TicketStatusEnum
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
            issue_description=f"Maintenance for {fake.word()}: {fake.text()}",
            status=random.choice(list(TicketStatusEnum)),
            device_id=random.choice(devices).id if devices else None,
            created_by_id=random.choice(employees).id,
            assigned_to_id=random.choice(employees).id
        )
        db.add(t)
    db.commit()
    print("Seeded Tickets")
