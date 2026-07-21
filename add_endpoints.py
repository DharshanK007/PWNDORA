import os

endpoints = {
    "employees.py": {
        "service": "employee",
        "actions": '''{
    "Pending": ["activate", "terminate"],
    "Active": ["suspend", "terminate"],
    "Suspended": ["activate", "terminate"],
    "Terminated": []
}'''
    },
    "devices.py": {
        "service": "device",
        "actions": '''{
    "New": ["register"],
    "Registered": ["configure"],
    "Configured": ["activate"],
    "Offline": ["activate"],
    "Maintenance": ["configure", "activate"],
    "Online": ["decommission"],
    "Decommissioned": []
}'''
    },
    "firmwares.py": {
        "service": "firmware",
        "actions": '''{
    "Draft": ["submit"],
    "Pending Approval": ["approve"],
    "Approved": ["deploy"],
    "Deployed": ["rollback"],
    "Retired": []
}'''
    },
    "tickets.py": {
        "service": "maintenance_ticket",
        "actions": '''{
    "Open": ["assign"],
    "Assigned": ["start"],
    "In Progress": ["resolve"],
    "Resolved": ["close"],
    "Closed": []
}'''
    },
    "inventory.py": {
        "service": "inventory",
        "actions": '''{
    "Created": ["allocate"],
    "Available": ["allocate"],
    "Restocked": ["allocate"],
    "Allocated": ["consume"],
    "Consumed": []
}'''
    },
    "reports.py": {
        "service": "report",
        "actions": '''{
    "Draft": ["approve"],
    "Under Review": ["approve"],
    "Approved": ["publish"],
    "Published": [],
    "Archived": []
}'''
    }
}

base_path = "backend/app/api/v1/endpoints"

for filename, data in endpoints.items():
    filepath = os.path.join(base_path, filename)
    with open(filepath, "r") as f:
        content = f.read()

    # Add WorkflowMetadataResponse import if missing
    if "WorkflowMetadataResponse" not in content:
        if "from app.schemas.base import PagedResponse" in content:
            content = content.replace(
                "from app.schemas.base import PagedResponse",
                "from app.schemas.base import PagedResponse, WorkflowMetadataResponse"
            )
        else:
            content = "from app.schemas.base import WorkflowMetadataResponse\n" + content

    endpoint_code = f'''
WORKFLOW_ACTIONS = {data['actions']}

@router.get("/{{id}}/workflow", response_model=WorkflowMetadataResponse)
def get_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    item = {data['service']}.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Entity not found")
    allowed = WORKFLOW_ACTIONS.get(item.status.value, [])
    return {{
        "current_state": item.status.value,
        "allowed_transitions": allowed
    }}
'''
    if "def get_workflow" not in content:
        content += "\n" + endpoint_code + "\n"
        
        with open(filepath, "w") as f:
            f.write(content)

print("Endpoints added successfully.")
