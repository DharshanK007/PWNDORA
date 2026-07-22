from app.db.session import SessionLocal
from app.scenarios.scenario_state_model import ScenarioState
from app.scenarios.scenario_registry import registry

def get_progressive_hint(scenario_state_id: str) -> str:
    """
    Reads the user's attempts and returns a progressive hint.
    """
    db = SessionLocal()
    try:
        state = db.query(ScenarioState).filter(ScenarioState.id == scenario_state_id).first()
        if not state:
            return "No active scenario state found."

        scenario = registry.get_scenario(state.scenario_id)
        stage_config = next((s for s in scenario.get("stages", []) if s.get("id") == state.current_stage), None)
        
        if not stage_config:
            return "No hints available for the current stage."
            
        attempts = state.attempts
        
        if attempts == 0:
            return "Take a look at the latest alerts or tickets."
        elif attempts < 3:
            return f"You might want to focus on the {stage_config.get('business_module', 'target')} module."
        else:
            # Reveal more about the discovery process
            return f"Hint: {stage_config.get('discovery_process', 'Look closely at the data returned by the endpoint.')}"
            
    finally:
        db.close()
