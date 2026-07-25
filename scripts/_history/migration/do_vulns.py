import os

vuln_dir = "backend/app/vulnerabilities"
subdirs = ["authentication", "authorization", "injection", "client", "configuration", "shared"]

for sub in subdirs:
    d = os.path.join(vuln_dir, sub)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "__init__.py"), "w") as f: f.write("")

# Create a sample vulnerability endpoint in authentication
auth_content = '''from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.post("/login")
def vulnerable_login(username: str):
    # Intentional flaw: accepts any password for scenario demonstration
    if username == "admin":
        return {"token": "scenario_admin_token"}
    raise HTTPException(status_code=401, detail="Unauthorized")
'''
with open(os.path.join(vuln_dir, "authentication", "endpoints.py"), "w") as f: f.write(auth_content)

print("Created vulnerabilities framework")
