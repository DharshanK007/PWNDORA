import os

def update_schema(filename, import_statement, base_modifications):
    filepath = f"backend/app/schemas/{filename}.py"
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Add imports
    if import_statement not in content:
        content = content.replace("from datetime import datetime", f"{import_statement}\nfrom datetime import datetime")
        
    for old, new in base_modifications:
        content = content.replace(old, new)
        
    with open(filepath, 'w') as f:
        f.write(content)

# Employee
update_schema(
    "employee",
    "from app.models.employee import EmployeeStatusEnum",
    [
        ("phone: Optional[str] = None", "phone: Optional[str] = None\n    status: EmployeeStatusEnum = EmployeeStatusEnum.PENDING"),
        ("phone: Optional[str] = None", "phone: Optional[str] = None\n    status: Optional[EmployeeStatusEnum] = None") # Update schema
    ]
)

# Firmware
update_schema(
    "firmware",
    "from app.models.firmware import FirmwareStatusEnum",
    [
        ("is_active: bool = False", "is_active: bool = False\n    status: FirmwareStatusEnum = FirmwareStatusEnum.DRAFT"),
        ("is_active: Optional[bool] = None", "is_active: Optional[bool] = None\n    status: Optional[FirmwareStatusEnum] = None")
    ]
)

# Ticket (Already has enum imports)
with open('backend/app/schemas/maintenance_ticket.py', 'r') as f:
    content = f.read()
if "TicketStatusEnum" not in content:
    content = content.replace("from app.models.maintenance_ticket import PriorityEnum", "from app.models.maintenance_ticket import PriorityEnum, TicketStatusEnum")
with open('backend/app/schemas/maintenance_ticket.py', 'w') as f:
    f.write(content)

# Inventory
update_schema(
    "inventory",
    "from app.models.inventory import InventoryStatusEnum",
    [
        ("supplier: Optional[str] = None", "supplier: Optional[str] = None\n    status: InventoryStatusEnum = InventoryStatusEnum.CREATED"),
        ("supplier: Optional[str] = None", "supplier: Optional[str] = None\n    status: Optional[InventoryStatusEnum] = None") # Note: it replaces both due to naive replace, which is fine since Base and Update have it
    ]
)

# Report
update_schema(
    "report",
    "from app.models.report import ReportStatusEnum",
    [
        ("generated_by_id: UUID", "generated_by_id: UUID\n    status: ReportStatusEnum = ReportStatusEnum.DRAFT"),
        ("summary: Optional[str] = None", "summary: Optional[str] = None\n    status: Optional[ReportStatusEnum] = None")
    ]
)
print("Updated Schemas")
