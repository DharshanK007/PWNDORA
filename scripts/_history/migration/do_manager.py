import os

base_dir = "backend/app/scenarios"
os.makedirs(base_dir, exist_ok=True)

# 1. Cache
cache_content = '''from typing import Any, Dict

class ScenarioCache:
    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def set(self, key: str, value: Any):
        self._cache[key] = value

    def clear(self, scenario_id: str = None):
        if scenario_id:
            keys_to_remove = [k for k in self._cache.keys() if k.startswith(f"{scenario_id}:")]
            for k in keys_to_remove:
                del self._cache[k]
        else:
            self._cache.clear()
'''
with open(os.path.join(base_dir, "scenario_cache.py"), "w") as f: f.write(cache_content)

# 2. Registry
registry_content = '''from typing import Dict, Any

class ScenarioRegistry:
    def __init__(self):
        self._scenarios: Dict[str, dict] = {}

    def register(self, scenario_id: str, data: dict):
        self._scenarios[scenario_id] = data

    def get_scenario(self, scenario_id: str) -> dict:
        return self._scenarios.get(scenario_id)

    def list_scenarios(self) -> list:
        return list(self._scenarios.values())
'''
with open(os.path.join(base_dir, "scenario_registry.py"), "w") as f: f.write(registry_content)

# 3. Loader
loader_content = '''import os
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
'''
with open(os.path.join(base_dir, "scenario_loader.py"), "w") as f: f.write(loader_content)

# 4. Executor
executor_content = '''from sqlalchemy.orm import Session
from .scenario_state_model import ScenarioState
from datetime import datetime, timezone
import uuid

class ScenarioExecutor:
    def start_scenario(self, db: Session, scenario_id: str, user_id: str) -> ScenarioState:
        # Check if already running
        existing = db.query(ScenarioState).filter(
            ScenarioState.scenario_id == scenario_id,
            ScenarioState.user_id == user_id,
            ScenarioState.status == "IN_PROGRESS"
        ).first()
        if existing:
            return existing
            
        state = ScenarioState(
            scenario_id=scenario_id,
            user_id=user_id,
            status="IN_PROGRESS",
            current_stage=1,
            started_at=datetime.now(timezone.utc)
        )
        db.add(state)
        db.commit()
        db.refresh(state)
        return state
'''
with open(os.path.join(base_dir, "scenario_executor.py"), "w") as f: f.write(executor_content)

# 5. Reset
reset_content = '''from sqlalchemy.orm import Session
from .scenario_state_model import ScenarioState
from .scenario_cache import ScenarioCache

class ScenarioReset:
    def __init__(self, cache: ScenarioCache):
        self.cache = cache

    def reset_scenario(self, db: Session, scenario_id: str, user_id: str):
        states = db.query(ScenarioState).filter(
            ScenarioState.scenario_id == scenario_id,
            ScenarioState.user_id == user_id
        ).all()
        for state in states:
            state.status = "RESET"
        db.commit()
        
        self.cache.clear(scenario_id)
'''
with open(os.path.join(base_dir, "scenario_reset.py"), "w") as f: f.write(reset_content)

# 6. Validator
validator_content = '''class ScenarioValidator:
    def validate_action(self, scenario_id: str, current_stage: int, action_data: dict) -> bool:
        # Placeholder for stage progression validation logic
        return True
'''
with open(os.path.join(base_dir, "scenario_validator.py"), "w") as f: f.write(validator_content)

# 7. Manager (Facade)
manager_content = '''from sqlalchemy.orm import Session
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
'''
with open(os.path.join(base_dir, "scenario_manager.py"), "w") as f: f.write(manager_content)

print("Created Scenario Manager modules")
