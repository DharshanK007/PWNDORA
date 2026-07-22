from app.db.session import SessionLocal
from app.models.report import Report, ReportStatusEnum
from app.scenarios.scenario_registry import registry
from app.scenarios.scenario_state_model import ScenarioState
from app.attack_engine.cvss import calculate_cvss
from app.attack_engine.owasp_risk import calculate_owasp_risk
from app.clues.clue_manager import clue_manager
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)

def generate_scenario_report(scenario_state_id: str, user_id: str):
    """
    Called when a ScenarioCompleted event is fired.
    Generates a draft report by gathering evidence, OWASP/MITRE/CVSS metrics.
    """
    db = SessionLocal()
    try:
        state = db.query(ScenarioState).filter(ScenarioState.id == scenario_state_id).first()
        if not state:
            return

        scenario = registry.get_scenario(state.scenario_id)
        if not scenario:
            return

        report_content = f"# Draft Report: {scenario.get('name')}\n\n"
        report_content += "## Business Context\n"
        report_content += f"{scenario.get('business_context')}\n\n"
        
        report_content += "## Findings\n\n"
        
        completed_stages = state.completed_stages or []
        for stage_id in completed_stages:
            stage_config = next((s for s in scenario.get("stages", []) if s.get("id") == stage_id), None)
            if not stage_config:
                continue
                
            report_content += f"### Stage {stage_id}: {stage_config.get('objective')}\n"
            report_content += f"- **OWASP Category**: {stage_config.get('owasp', 'N/A')}\n"
            report_content += f"- **MITRE Technique**: {stage_config.get('mitre', 'N/A')}\n"
            
            # CVSS
            cvss_metrics = stage_config.get("cvss")
            if cvss_metrics:
                cvss_score = calculate_cvss(cvss_metrics)
                report_content += f"- **CVSS v3.1 Base Score**: {cvss_score}\n"
            
            # OWASP Risk
            risk_factors = stage_config.get("owasp_risk_factors")
            if risk_factors:
                l_score, i_score, risk_lvl = calculate_owasp_risk(risk_factors)
                report_content += f"- **OWASP Risk Level**: {risk_lvl} (Likelihood: {l_score}, Impact: {i_score})\n"
                
            # Evidence
            evidence = stage_config.get("evidence", [])
            if evidence:
                report_content += "- **Evidence Collected**:\n"
                for ev in evidence:
                    report_content += f"  - [{ev.get('type')}] {ev.get('name')}\n"
                    
            report_content += "\n#### Analyst Notes (Placeholder)\n"
            report_content += "[Write your technical analysis here]\n\n"
            report_content += "#### Recommendations (Placeholder)\n"
            report_content += "[Write remediation recommendations here]\n\n"

        # Create Draft Report
        # Determine the user's employee record to link it
        from app.models.user import User
        user = db.query(User).filter(User.id == user_id).first()
        employee_id = user.employee.id if user and user.employee else None

        new_report = Report(
            id=str(uuid4()),
            title=f"Scenario Report: {scenario.get('name')}",
            report_type="Vulnerability Assessment",
            file_path="",  # Or a path if we were saving to disk, but we use summary for now
            summary=report_content,
            status=ReportStatusEnum.DRAFT,
            generated_by_id=employee_id,
            scenario_state_id=scenario_state_id
        )
        db.add(new_report)
        db.commit()
        
    except Exception as e:
        logger.error(f"Failed to generate scenario report: {e}")
    finally:
        db.close()
