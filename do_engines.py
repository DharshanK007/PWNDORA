import os

# 1. Challenge Engine
ce_dir = "backend/app/challenge_engine"
os.makedirs(ce_dir, exist_ok=True)

with open(os.path.join(ce_dir, "__init__.py"), "w") as f: f.write("")

sm_content = '''class StageManager:
    def __init__(self):
        pass

    def get_current_stage(self, scenario_id: str, current_stage_idx: int) -> dict:
        # returns the configuration for the current stage
        return {}
'''
with open(os.path.join(ce_dir, "stage_manager.py"), "w") as f: f.write(sm_content)

tr_content = '''class TransitionRules:
    def check_transition(self, current_stage: dict, action_data: dict) -> bool:
        # logic to see if action satisfies transition rules
        return True
'''
with open(os.path.join(ce_dir, "transition.py"), "w") as f: f.write(tr_content)

val_content = '''class ChallengeValidator:
    def validate(self, rule: dict, action: dict) -> bool:
        return True
'''
with open(os.path.join(ce_dir, "validator.py"), "w") as f: f.write(val_content)

# 2. Clue Engine
clue_dir = "backend/app/clues"
os.makedirs(clue_dir, exist_ok=True)
with open(os.path.join(clue_dir, "__init__.py"), "w") as f: f.write("")

ct_content = '''from enum import Enum

class ClueType(str, Enum):
    TICKET = "Ticket"
    NOTE = "Employee Note"
    CONFIG = "Configuration"
    BACKUP = "Backup"
    FIRMWARE = "Firmware"
    EMAIL = "Email"
    DOCUMENTATION = "Documentation"
    AUDIT_LOG = "Audit Log"
    NETWORK_DIAGRAM = "Network Diagram"
    API_RESPONSE = "API Response"
'''
with open(os.path.join(clue_dir, "clue_types.py"), "w") as f: f.write(ct_content)

cp_content = '''from .clue_types import ClueType

class ClueProvider:
    def get_clue(self, clue_id: str, clue_type: ClueType) -> dict:
        return {"id": clue_id, "type": clue_type, "content": "Sample Clue Content"}
'''
with open(os.path.join(clue_dir, "clue_provider.py"), "w") as f: f.write(cp_content)

cv_content = '''class ClueValidator:
    def is_clue_unlocked(self, clue_id: str, user_progress: int) -> bool:
        return True
'''
with open(os.path.join(clue_dir, "clue_validator.py"), "w") as f: f.write(cv_content)

cm_content = '''from .clue_provider import ClueProvider
from .clue_validator import ClueValidator

class ClueManager:
    def __init__(self):
        self.provider = ClueProvider()
        self.validator = ClueValidator()

    def request_clue(self, clue_id: str, user_progress: int):
        if self.validator.is_clue_unlocked(clue_id, user_progress):
            return self.provider.get_clue(clue_id, None)
        return None

clue_manager = ClueManager()
'''
with open(os.path.join(clue_dir, "clue_manager.py"), "w") as f: f.write(cm_content)

print("Created Challenge and Clue Engines")
