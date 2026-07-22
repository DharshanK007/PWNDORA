from app.db.session import SessionLocal
from app.models.user import User

def explain_capabilities(user_id: str) -> str:
    """
    Reads the user's capability graph and provides a plain-language explanation.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.capabilities:
            return "You haven't unlocked any special capabilities yet."
            
        caps = user.capabilities
        explanation = "Here is what you are currently capable of:\n"
        for cap, details in caps.items():
            explanation += f"- **{cap}**: Unlocked in scenario {details.get('scenario_id')}\n"
            
        return explanation
    finally:
        db.close()
