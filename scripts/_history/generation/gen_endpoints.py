import os

def append_to_file(filename, content):
    with open(f"backend/app/api/v1/endpoints/{filename}.py", "a") as f:
        f.write("\n" + content)

# Employees
append_to_file("employees", '''
@router.post("/{id}/activate", response_model=EmployeeResponse)
def activate_employee_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = employee.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.activate(db, db_obj=item)

@router.post("/{id}/terminate", response_model=EmployeeResponse)
def terminate_employee_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = employee.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.terminate(db, db_obj=item)
''')

# Devices
append_to_file("devices", '''
@router.post("/{id}/register", response_model=DeviceResponse)
def register_device_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    return device.register(db, db_obj=item)

@router.post("/{id}/configure", response_model=DeviceResponse)
def configure_device_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    return device.configure(db, db_obj=item)

@router.post("/{id}/activate", response_model=DeviceResponse)
def activate_device_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    return device.activate(db, db_obj=item)

@router.post("/{id}/decommission", response_model=DeviceResponse)
def decommission_device_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = device.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    return device.decommission(db, db_obj=item)
''')

# Firmwares
append_to_file("firmwares", '''
@router.post("/{id}/submit", response_model=FirmwareResponse)
def submit_firmware_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = firmware.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Firmware not found")
    return firmware.submit(db, db_obj=item)

@router.post("/{id}/approve", response_model=FirmwareResponse)
def approve_firmware_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR]))
) -> Any:
    item = firmware.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Firmware not found")
    return firmware.approve(db, db_obj=item)

@router.post("/{id}/deploy", response_model=FirmwareResponse)
def deploy_firmware_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = firmware.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Firmware not found")
    return firmware.deploy(db, db_obj=item)
''')

# Tickets
append_to_file("tickets", '''
from pydantic import BaseModel
class AssignRequest(BaseModel):
    engineer_id: UUID

class ResolveRequest(BaseModel):
    resolution_notes: str

@router.post("/{id}/assign", response_model=MaintenanceTicketResponse)
def assign_ticket_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    assign_req: AssignRequest,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return maintenance_ticket.assign(db, db_obj=item, engineer_id=assign_req.engineer_id)

@router.post("/{id}/start", response_model=MaintenanceTicketResponse)
def start_ticket_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return maintenance_ticket.start(db, db_obj=item)

@router.post("/{id}/resolve", response_model=MaintenanceTicketResponse)
def resolve_ticket_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    resolve_req: ResolveRequest,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.ENGINEER]))
) -> Any:
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return maintenance_ticket.resolve(db, db_obj=item, resolution_notes=resolve_req.resolution_notes)

@router.post("/{id}/close", response_model=MaintenanceTicketResponse)
def close_ticket_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER]))
) -> Any:
    item = maintenance_ticket.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return maintenance_ticket.close(db, db_obj=item)
''')

# Inventory
append_to_file("inventory", '''
from pydantic import BaseModel
class QuantityRequest(BaseModel):
    quantity: int

@router.post("/{id}/allocate", response_model=InventoryResponse)
def allocate_inventory_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    req: QuantityRequest,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER, RoleEnum.ENGINEER]))
) -> Any:
    item = inventory.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory.allocate(db, db_obj=item, quantity=req.quantity)

@router.post("/{id}/consume", response_model=InventoryResponse)
def consume_inventory_endpoint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user = Depends(deps.RoleChecker([RoleEnum.ADMINISTRATOR, RoleEnum.MANAGER, RoleEnum.ENGINEER]))
) -> Any:
    item = inventory.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory.consume(db, db_obj=item)
''')

# Reports
append_to_file("reports", '''
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
''')
print("Appended endpoints")
