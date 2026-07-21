from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.post("/login")
def vulnerable_login(username: str):
    # Intentional flaw: accepts any password for scenario demonstration
    if username == "admin":
        return {"token": "scenario_admin_token"}
    raise HTTPException(status_code=401, detail="Unauthorized")
