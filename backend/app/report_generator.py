from app.db.session import SessionLocal
from app.models.report import Report, ReportStatusEnum
from app.scenarios.scenario_manager import manager
from app.scenarios.scenario_state_model import ScenarioState
from app.attack_engine.cvss import calculate_cvss
from app.attack_engine.owasp_risk import calculate_owasp_risk
from app.clues.clue_manager import clue_manager
import logging
from uuid import uuid4
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

STAGE_HINTS = {
  1: [
    "Apply reasonable filters (e.g., Status: Maintenance, Group: Production) in assets to narrow down the list.",
    "Check for the patch date carefully; the targeted asset will be noticeably older than the decoys."
  ],
  2: [
    "Use the assigned job role to search for the employee in the Employees section who is assigned in the Assets section.",
    "Look closely at the internal note in the employee profile. It contains an incident reference and a clue about where the firmware activity was recorded."
  ],
  3: [
    'Use the leaked internal note as your pivot. Search for firmware-related deployment evidence connected to the Line 2 halt and ticket #402.',
    'Probe the Search bar with an injection-style query such as " OR 1=1 -- and watch for deployment audit events that should not be visible to your account.'
  ],
  4: [
    "Intercept the firmware update request using the browser's developer tools.",
    "Modify the X-User-Role header in your request from 'Engineer' to 'Administrator' and resend the request."
  ]
}

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
        
        # Calculate time analysis
        time_analysis = "N/A"
        if state.started_at:
            end_time = state.completed_at or datetime.now(timezone.utc)
            duration = end_time - state.started_at
            minutes = int(duration.total_seconds() // 60)
            seconds = int(duration.total_seconds() % 60)
            time_analysis = f"{minutes} minutes and {seconds} seconds"

        report_content = f"# PenTest-Vulnerability Assessment: {scenario.get('name')}\n\n"
        report_content += "## Engagement Executive Summary & Business Context\n"
        report_content += f"{scenario.get('business_context')}\n\n"
        report_content += f"**Time Analysis (Total Engagement Duration):** {time_analysis}\n\n"
        report_content += "This deliverable documents the technical vulnerability findings, attack vectors, risk metrics, and mitigation guidelines produced during the NeoFactory Industrial Cyber Range assessment.\n\n"
        
        report_content += "## Consolidated Finding Matrix & Attack Chain\n\n"
        
        completed_stages = state.completed_stages or []
        if not completed_stages:
            return None
            
        # Variables for Learner Assessment
        learner_assessment_content = "## Learner Assessment (MATRIX Score)\n\n"
        learner_assessment_content += "This section evaluates learner performance, efficiency, and threat understanding across the engagement.\n\n"
        
        meta = state.metadata_json or {}
        answers = meta.get("answers", {})
        start_times = meta.get("stage_start_times", {})
        end_times = meta.get("stage_completion_times", {})
        
        # Generate Findings Section
        report_content += "## Threat Assessment\n\n"
        report_content += "This section outlines the attack chain progression, vulnerabilities discovered, and mapped threat intelligence frameworks.\n\n"
        
        stages_counted = 0
        lab_matrix_total = 0
        
        # Collection for infographics payload
        infographics_data = []

        for stage_id in completed_stages:
            stage_config = next((s for s in scenario.get("stages", []) if s.get("id") == stage_id), None)
            if not stage_config:
                continue
                
            report_content += f"### Stage #{stage_id}: **{stage_config.get('objective')}**\n"
            report_content += f"- **Enterprise Layer**: {stage_config.get('enterprise_layer', stage_config.get('business_module', 'N/A'))}\n"
            report_content += f"- **Attack Surface**: {stage_config.get('attack_surface', stage_config.get('target_endpoint', 'N/A'))}\n"
            report_content += f"- **Discovery Surface**: {stage_config.get('discovery_surface', stage_config.get('discovery_process', 'N/A'))}\n"
            report_content += f"- **Technical Mechanism**: {stage_config.get('technical_mechanism', 'N/A')}\n"
            report_content += f"- **Capability Gained**: {stage_config.get('capability_gained', 'N/A')}\n"
            
            owasp = stage_config.get('owasp', 'N/A')
            report_content += f"- **OWASP Classification**: {owasp}\n"
            
            mitre = stage_config.get('mitre', 'N/A')
            report_content += f"- **MITRE ATT&CK Mapping**: {mitre}\n"
            
            # Selected Primary Technique (from answers)
            stage_answers = answers.get(str(stage_id), {})
            selected_mitre = stage_answers.get("mitre", "None selected")
            report_content += f"- **Selected Primary Technique**: {selected_mitre}\n"
            
            cvss = stage_config.get("cvss", {})
            if cvss:
                from app.core.metrics import calculate_cvss_v3_1
                cvss_score = calculate_cvss_v3_1(cvss)
                report_content += f"- **CVSS v3.1 Base Score**: **{cvss_score:.1f} / 10.0**\n"
                
            owasp_likelihood = stage_config.get("owasp_risk_factors", {}).get("likelihood")
            owasp_impact = stage_config.get("owasp_risk_factors", {}).get("impact")
            if owasp_likelihood is not None and owasp_impact is not None:
                from app.core.metrics import get_owasp_risk_rating
                rating = get_owasp_risk_rating(owasp_likelihood, owasp_impact)
                report_content += f"- **OWASP Risk Rating**: **{rating}** (Likelihood: {owasp_likelihood}/10, Impact: {owasp_impact}/10)\n"
                
            evidence = stage_config.get("evidence", [])
            report_content += f"- **Technical Evidence Collected**:\n"
            if evidence:
                for ev in evidence:
                    report_content += f"  - `{ev}`\n"
            else:
                report_content += "  - None\n"
                
            report_content += "\n---\n\n"
            
            # Learner MATRIX Analytics calculation
            used_indices = state.hints_used.get(str(stage_id), []) if state.hints_used else []
            hint_count = len(used_indices)
            hint_efficiency = 100 if hint_count == 0 else (50 if hint_count == 1 else 0)
            
            start_iso = start_times.get(str(stage_id))
            end_iso = end_times.get(str(stage_id))
            time_efficiency = 0
            time_taken_str = "N/A"
            diff_seconds_val = 0
            if start_iso and end_iso:
                try:
                    s_time = datetime.fromisoformat(start_iso.replace('Z', '+00:00'))
                    e_time = datetime.fromisoformat(end_iso.replace('Z', '+00:00'))
                    diff_seconds = (e_time - s_time).total_seconds()
                    diff_seconds_val = diff_seconds
                    minutes = diff_seconds / 60.0
                    degradation = max(0, (minutes - 10) * 5)
                    time_efficiency = max(0, min(100, 100 - degradation))
                    time_taken_str = f"{int(minutes)}m {int(diff_seconds % 60)}s"
                except Exception:
                    pass

            gt = stage_config.get("evaluation_ground_truth")
            accuracy = 0
            if gt:
                correct = 0
                total = 0
                if stage_answers.get("mitre") == gt.get("mitre", {}).get("answer"):
                    correct += 1
                total += 1
                for k, v in gt.get("cvss", {}).items():
                    if stage_answers.get(k) == v: correct += 1
                    total += 1
                for k, v in gt.get("owasp_likelihood", {}).items():
                    if stage_answers.get(k) == v: correct += 1
                    total += 1
                for k, v in gt.get("owasp_impact", {}).items():
                    if stage_answers.get(k) == v: correct += 1
                    total += 1
                if total > 0:
                    accuracy = (correct / total) * 100
                    
            tech_acc = accuracy
            threat_und = accuracy
            
            stage_matrix = (hint_efficiency + time_efficiency + tech_acc + threat_und) / 4.0
            lab_matrix_total += stage_matrix
            stages_counted += 1
            
            infographics_data.append({
                "stage": stage_id,
                "matrix": round(stage_matrix, 1),
                "time": int(diff_seconds_val)
            })
            
            learner_assessment_content += f"### Stage {stage_id} MATRIX Score: **{stage_matrix:.1f}/100**\n"
            learner_assessment_content += f"- **Hint Efficiency**: **{hint_efficiency:.1f}%** ({hint_count} hints used)\n"
            learner_assessment_content += f"- **Time Efficiency**: **{time_efficiency:.1f}%** ({time_taken_str})\n"
            learner_assessment_content += f"- **Technical Accuracy**: **{tech_acc:.1f}%**\n"
            learner_assessment_content += f"- **Threat Understanding**: **{threat_und:.1f}%**\n\n"

        if stages_counted > 0:
            final_matrix = lab_matrix_total / stages_counted
            learner_assessment_content += f"### FINAL LAB MATRIX SCORE: **{final_matrix:.1f}/100**\n\n"
            
        report_content += learner_assessment_content
        
        import json
        report_content += "\n\n<!-- [INFOGRAPHICS_DATA]\n" + json.dumps(infographics_data) + "\n-->\n"

        # Create Draft Report
        from app.models.user import User
        user = db.query(User).filter(User.id == actual_user_id).first()
        employee_id = user.employee.id if user and user.employee else None

        # Delete any previous reports for this user so only the current session is kept
        if employee_id:
            db.query(Report).filter(Report.generated_by_id == employee_id).delete(synchronize_session=False)
            db.commit()

        new_report = Report(
            id=str(uuid4()),
            title=f"PenTest-Vulnerability Assessment: {scenario.get('name')}",
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
