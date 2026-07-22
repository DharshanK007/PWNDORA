from app.db.session import SessionLocal
from app.models.report import Report, ReportStatusEnum
from app.scenarios.scenario_manager import manager
from app.scenarios.scenario_state_model import ScenarioState
from app.attack_engine.cvss import calculate_cvss
from app.attack_engine.owasp_risk import calculate_owasp_risk
from app.clues.clue_manager import clue_manager
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)

def generate_scenario_report(scenario_state_id: str, user_id: str = None):
    """
    Called when a ScenarioCompleted event is fired or on reports query.
    Generates a draft report by gathering evidence, OWASP/MITRE/CVSS metrics.
    """
    import os
    if not manager.registry.list_scenarios():
        data_dir = os.path.join(os.path.dirname(__file__), "scenario_data")
        if os.path.exists(data_dir):
            manager.load_all(data_dir)

    db = SessionLocal()
    try:
        state = db.query(ScenarioState).filter(ScenarioState.id == scenario_state_id).first()
        if not state:
            return None

        # Check if a report already exists for this state
        existing = db.query(Report).filter(Report.scenario_state_id == scenario_state_id).first()
        if existing:
            return existing

        scenario = manager.registry.get_scenario(state.scenario_id)
        if not scenario:
            return None

        actual_user_id = str(user_id or state.user_id)
        report_content = f"# Professional Vulnerability Assessment Report: {scenario.get('name')}\n\n"
        report_content += "## Engagement Executive Summary & Business Context\n"
        report_content += f"{scenario.get('business_context')}\n\n"
        report_content += "This deliverable documents the technical vulnerability findings, attack vectors, risk metrics, and mitigation guidelines produced during the NeoFactory Industrial Cyber Range assessment.\n\n"
        
        report_content += "## Consolidated Finding Matrix & Attack Chain\n\n"
        
        completed_stages = state.completed_stages or [1, 2, 3, 4]
        for stage_id in completed_stages:
            stage_config = next((s for s in scenario.get("stages", []) if s.get("id") == stage_id), None)
            if not stage_config:
                continue
                
            report_content += f"### Finding #{stage_id}: {stage_config.get('objective')}\n"
            report_content += f"- **Enterprise Layer**: {stage_config.get('enterprise_layer', stage_config.get('business_module', 'N/A'))}\n"
            report_content += f"- **Attack Surface**: {stage_config.get('attack_surface', stage_config.get('target_endpoint', 'N/A'))}\n"
            report_content += f"- **Discovery Surface**: {stage_config.get('discovery_surface', stage_config.get('discovery_process', 'N/A'))}\n"
            report_content += f"- **Technical Mechanism**: {stage_config.get('technical_mechanism', 'Unsanitized input or session control flaw')}\n"
            report_content += f"- **Capability Gained**: {stage_config.get('capability_gained', 'N/A')}\n"
            report_content += f"- **OWASP Classification**: {stage_config.get('owasp', 'N/A')}\n"
            report_content += f"- **MITRE ATT&CK Mapping**: {stage_config.get('mitre', 'N/A')}\n"
            
            # CVSS
            cvss_metrics = stage_config.get("cvss")
            if cvss_metrics:
                cvss_score = calculate_cvss(cvss_metrics)
                report_content += f"- **CVSS v3.1 Base Score**: {cvss_score} / 10.0\n"
            else:
                report_content += f"- **CVSS v3.1 Base Score**: 7.5 (High)\n"
            
            # OWASP Risk
            risk_factors = stage_config.get("owasp_risk_factors")
            if risk_factors:
                l_score, i_score, risk_lvl = calculate_owasp_risk(risk_factors)
                report_content += f"- **OWASP Risk Rating**: {risk_lvl} (Likelihood: {l_score}/10, Impact: {i_score}/10)\n"
            else:
                report_content += f"- **OWASP Risk Rating**: HIGH (Likelihood: 7/10, Impact: 7/10)\n"
                
            # Evidence
            evidence = stage_config.get("evidence", [])
            if evidence:
                report_content += "- **Technical Evidence Collected**:\n"
                for ev in evidence:
                    report_content += f"  - `[{ev}]`\n"
                    
            report_content += "\n#### Analyst Technical Assessment\n"
            report_content += "[Write your technical analysis here]\n\n"
            report_content += "#### Remediation & Control Guidance\n"
            report_content += "[Write remediation recommendations here]\n\n"

        # Create Draft Report
        from app.models.user import User
        user = db.query(User).filter(User.id == actual_user_id).first()
        employee_id = user.employee.id if user and user.employee else None

        new_report = Report(
            id=str(uuid4()),
            title=f"Assessment Report: {scenario.get('name')}",
            report_type="Vulnerability Assessment",
            file_path="/reports/draft.pdf",
            summary=report_content,
            status=ReportStatusEnum.DRAFT,
            generated_by_id=employee_id,
            scenario_state_id=scenario_state_id
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report
        
    except Exception as e:
        logger.error(f"Failed to generate scenario report: {e}")
    finally:
        db.close()
