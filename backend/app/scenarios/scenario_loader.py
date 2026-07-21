import os
import yaml
from .scenario_registry import ScenarioRegistry

class ScenarioLoader:
    def __init__(self, registry: ScenarioRegistry):
        self.registry = registry

    def load_from_directory(self, data_dir: str):
        if not os.path.exists(data_dir):
            return
        for item in os.listdir(data_dir):
            scenario_path = os.path.join(data_dir, item)
            yaml_path = os.path.join(scenario_path, "scenario.yaml")
            if os.path.isdir(scenario_path) and os.path.exists(yaml_path):
                with open(yaml_path, "r") as f:
                    data = yaml.safe_load(f)
                    self.registry.register(data.get("id"), data)
