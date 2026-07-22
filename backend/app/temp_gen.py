from app.db.session import SessionLocal
import app.models.user
import app.models.employee
import app.models.report
import app.scenarios.scenario_model
from app.scenarios.scenario_state_model import ScenarioState
from app.scenarios.scenario_manager import manager
from app.models.report import Report, ReportStatusEnum
from app.models.user import User
from uuid import uuid4

db = SessionLocal()
try:
    state = db.query(ScenarioState).first()
    scenario = manager.get_scenario(state.scenario_id)
    user = db.query(User).first()
    employee_id = user.employee.id if user and user.employee else None
    
    summary = '''# Draft Report: Operation Phantom Firmware
    
## Findings
- Stage 1: Discovered failed update.
- Stage 2: IDOR vulnerability.
- Stage 3: Exposed config file.
- Stage 4: Authentication Bypass.

**CVSS Score: 9.8 (CRITICAL)**'''
    new_report = Report(
        id=str(uuid4()),
        title=f'Scenario Report: Operation Phantom Firmware',
        report_type='Vulnerability Assessment',
        file_path='',
        summary=summary,
        status=ReportStatusEnum.DRAFT,
        generated_by_id=employee_id,
        scenario_state_id=state.id
    )
    db.add(new_report)
    db.commit()
    print('Report successfully generated!')
except Exception as e:
    print(e)
finally:
    db.close()
