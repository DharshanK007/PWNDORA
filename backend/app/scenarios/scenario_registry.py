from typing import Dict, Any

class ScenarioRegistry:
    def __init__(self):
        self._scenarios: Dict[str, dict] = {}

    def register(self, scenario_id: str, data: dict):
        self._scenarios[scenario_id] = data

    def get_scenario(self, scenario_id: str) -> dict:
        return self._scenarios.get(scenario_id)

    def list_scenarios(self) -> list:
        return list(self._scenarios.values())
