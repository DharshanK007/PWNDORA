import os

base_path = "backend/app/api/v1/endpoints"
files_to_update = ["employees.py", "devices.py", "firmwares.py", "tickets.py", "inventory.py", "reports.py"]

for filename in files_to_update:
    filepath = os.path.join(base_path, filename)
    with open(filepath, "r") as f:
        content = f.read()

    if "from typing import List" not in content and "from typing import" in content:
        content = content.replace("from typing import ", "from typing import List, ")
    elif "from typing import" not in content:
        content = "from typing import List\n" + content

    if "WorkflowHistoryResponse" not in content:
        content = "from app.schemas.workflow_history import WorkflowHistoryResponse\n" + content

    with open(filepath, "w") as f:
        f.write(content)

print("Fixed imports")
