from app.api.dependencies.query import QueryParameters, get_query_parameters
from app.schemas.workflow_history import WorkflowHistoryResponse
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.models.user import RoleEnum
from app.schemas.base import PagedResponse, WorkflowMetadataResponse
from app.schemas.report import ReportCreate, ReportUpdate, ReportResponse
from app.services import report

router = APIRouter()

@router.get("/", response_model=PagedResponse[ReportResponse])
def read_reports(
    db: Session = Depends(deps.get_db),
    params: QueryParameters = Depends(get_query_parameters),
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve reports.
    """
    items = report.get_multi(db, params=params)
    total = report.get_count(db, params=params)
    return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    *,
    db: Session = Depends(deps.get_db),
    item_in: ReportCreate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Create new report.
    """
    item = report.create(db, obj_in=item_in)
    return item

@router.put("/{id}", response_model=ReportResponse)
def update_report(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: ReportUpdate,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Update an existing report.
    """
    item = report.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Report not found")
    item = report.update(db, db_obj=item, obj_in=item_in)
    return item

@router.get("/{id}", response_model=ReportResponse)
def read_report(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Get report by ID.
    """
    item = report.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Report not found")
    return item

@router.delete("/{id}", response_model=ReportResponse)
def delete_report(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    """
    Delete a report.
    """
    item = report.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Report not found")
    item = report.remove(db, id=id)
    return item


@router.post("/{id}/approve", response_model=ReportResponse)
def approve_report_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = report.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Report not found")
    return report.approve(db, db_obj=item)

@router.post("/{id}/publish", response_model=ReportResponse)
def publish_report_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = report.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Report not found")
    return report.publish(db, db_obj=item)

@router.post("/{id}/archive", response_model=ReportResponse)
def archive_report_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = report.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Report not found")
    return report.archive(db, db_obj=item)


WORKFLOW_ACTIONS = {
    "Draft": ["approve"],
    "Under Review": ["approve"],
    "Approved": ["publish"],
    "Published": [],
    "Archived": []
}

@router.get("/{id}/workflow", response_model=WorkflowMetadataResponse)
def get_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    item = report.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Entity not found")
    allowed = WORKFLOW_ACTIONS.get(item.status.value, [])
    return {
        "current_state": item.status.value,
        "allowed_transitions": allowed
    }



@router.get("/{id}/history", response_model=List[WorkflowHistoryResponse])
def get_history(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.get_current_user)
) -> Any:
    from app.services.workflow_history import WorkflowHistoryService
    return WorkflowHistoryService.get_history_for_entity(db, "reports", str(id))

