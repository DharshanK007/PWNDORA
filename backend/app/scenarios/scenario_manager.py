from sqlalchemy.orm import Session
from .scenario_registry import ScenarioRegistry
from .scenario_loader import ScenarioLoader
from .scenario_executor import ScenarioExecutor
from .scenario_reset import ScenarioReset
from .scenario_validator import ScenarioValidator
from .scenario_cache import ScenarioCache

class ScenarioManager:
    def __init__(self):
        self.registry = ScenarioRegistry()
        self.loader = ScenarioLoader(self.registry)
        self.cache = ScenarioCache()
        self.executor = ScenarioExecutor()
        self.reset_service = ScenarioReset(self.cache)
        self.validator = ScenarioValidator()

    def load_all(self, data_dir: str):
        self.loader.load_from_directory(data_dir)

    def start(self, db: Session, scenario_id: str, user_id: str):
        return self.executor.start_scenario(db, scenario_id, user_id)

    def reset(self, db: Session, scenario_id: str, user_id: str):
        return self.reset_service.reset_scenario(db, scenario_id, user_id)

# Global Instance
manager = ScenarioManager()
