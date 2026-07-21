from fastapi import status
from app.core.exceptions import NeoFactoryException

def validate_transition(current_state: str, target_state: str, allowed_transitions: dict[str, list[str]]):
    """
    Validates if a transition from current_state to target_state is allowed based on the allowed_transitions map.
    """
    if current_state == target_state:
        raise NeoFactoryException(
            message=f"Entity is already in {target_state} state",
            status_code=status.HTTP_400_BAD_REQUEST
        )
        
    allowed_next_states = allowed_transitions.get(current_state, [])
    if target_state not in allowed_next_states:
        raise NeoFactoryException(
            message=f"Invalid transition from {current_state} to {target_state}",
            status_code=status.HTTP_400_BAD_REQUEST
        )

def require_condition(condition: bool, error_message: str):
    """
    Raises a 400 Bad Request exception if the condition is not met.
    """
    if not condition:
        raise NeoFactoryException(
            message=error_message,
            status_code=status.HTTP_400_BAD_REQUEST
        )
