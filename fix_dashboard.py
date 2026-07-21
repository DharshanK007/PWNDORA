import os

filepath = "backend/app/api/v1/endpoints/dashboard.py"
with open(filepath, "r") as f: content = f.read()

if "from app.models.user import User" not in content:
    content = content.replace("from sqlalchemy.orm import Session", "from sqlalchemy.orm import Session\nfrom app.models.user import User")
    with open(filepath, "w") as f: f.write(content)

print("Fixed dashboard imports")
