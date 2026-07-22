from typing import Dict, Any

class TransitionRules:
    def check_transition(self, current_stage: Dict[str, Any], action_data: Dict[str, Any]) -> bool:
        stage_id = current_stage.get("id")
        
        if stage_id == 1:
            # Assets reading Line 2 device
            return True
            
        elif stage_id == 2:
            # Employees reading engineer record
            return True
            
        elif stage_id == 3:
            # Search injection
            query = action_data.get("query", "").lower()
            # Accept SQL injection patterns or searching for firmware/logs
            if any(term in query for term in ["'", "or", "1=1", "%", "firmware", "select", "deploy", "log", "--", "union"]):
                return True
            return False
            
        elif stage_id == 4:
            # Auth escalation
            role = action_data.get("role") or action_data.get("header_role")
            if role in ["Administrator", "ADMINISTRATOR", "admin", "Admin"]:
                return True
            return False
            
        return True
