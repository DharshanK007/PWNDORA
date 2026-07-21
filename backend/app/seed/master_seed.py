import os
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
