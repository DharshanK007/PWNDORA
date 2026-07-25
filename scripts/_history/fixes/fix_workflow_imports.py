import os

base_path = "backend/app/api/v1/endpoints"
files_to_update = ["employees.py", "devices.py", "firmwares.py", "tickets.py", "inventory.py", "reports.py"]

for filename in files_to_update:
    filepath = os.path.join(base_path, filename)
    with open(filepath, "r") as f:
        content = f.read()

    if "from app.schemas.workflow_history import WorkflowHistoryResponse" not in content:
        content = "from app.schemas.workflow_history import WorkflowHistoryResponse\n" + content
        with open(filepath, "w") as f:
            f.write(content)

print("Fixed WorkflowHistoryResponse imports")
