import os

filepath = "backend/app/api/v1/endpoints/dashboard.py"
with open(filepath, "r") as f: content = f.read()

if "/organization" not in content:
    endpoints = '''
@router.get("/organization")
def get_dashboard_organization(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated organization metrics"}

@router.get("/network")
def get_dashboard_network(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated network metrics"}

@router.get("/security")
def get_dashboard_security(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated security metrics"}

@router.get("/activity")
def get_dashboard_activity(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated activity metrics"}

@router.get("/operations")
def get_dashboard_operations(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated operations metrics"}

@router.get("/statistics")
def get_dashboard_statistics(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return {"status": "ok", "message": "Aggregated statistics metrics"}
'''
    content = content + endpoints
    with open(filepath, "w") as f: f.write(content)

print("Updated dashboard endpoints")
