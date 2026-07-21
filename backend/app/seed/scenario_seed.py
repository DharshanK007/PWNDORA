from app.scenarios.scenario_model import Scenario
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
