from app.hint_engine import get_progressive_hint
from app.explainer import explain_capabilities

def ask_mentor(user_id: str, scenario_state_id: str, question: str) -> str:
    """
    Conversational wrapper around the hint engine and explainer.
    Nudges the learner based on their attempts and capabilities.
    """
    # Simple keyword routing for the mock AI
    q = question.lower()
    
    if "help" in q or "stuck" in q or "hint" in q:
        return f"Mentor: {get_progressive_hint(scenario_state_id)}"
    elif "capable" in q or "what can i do" in q or "abilities" in q:
        return f"Mentor: {explain_capabilities(user_id)}"
    else:
        return "Mentor: I'm here to help. You can ask for a 'hint' if you're stuck, or ask 'what can I do' to review your capabilities."
