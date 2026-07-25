import os

base_path = "backend/app/api/v1/endpoints"
files_to_update = ["employees.py", "devices.py", "firmwares.py", "tickets.py", "inventory.py", "reports.py"]

for filename in files_to_update:
    filepath = os.path.join(base_path, filename)
    with open(filepath, "r") as f:
        content = f.read()

    # Add WorkflowHistoryResponse import if missing
    if "WorkflowHistoryResponse" not in content:
        if "from app.schemas.base import WorkflowMetadataResponse" in content:
            content = content.replace(
                "from app.schemas.base import WorkflowMetadataResponse",
                "from app.schemas.base import WorkflowMetadataResponse\nfrom app.schemas.workflow_history import WorkflowHistoryResponse\nfrom typing import List"
            )
        
    entity_name = filename.split('.')[0]
    
    endpoint_code = f'''
@router.get("/{{id}}/history", response_model=List[WorkflowHistoryResponse])
def get_history(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    from app.services.workflow_history import WorkflowHistoryService
    return WorkflowHistoryService.get_history_for_entity(db, "{entity_name}", str(id))
'''
    if "def get_history(" not in content:
        content += "\n" + endpoint_code + "\n"
        with open(filepath, "w") as f:
            f.write(content)

print("Added /history endpoints.")
