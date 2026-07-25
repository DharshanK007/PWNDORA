import os
import re

def update_device():
    with open('backend/app/models/device.py', 'r') as f:
        content = f.read()
    
    old_enum = '''class DeviceStatusEnum(str, enum.Enum):
    ONLINE = "Online"
    OFFLINE = "Offline"
    MAINTENANCE = "Maintenance"'''
    
    new_enum = '''class DeviceStatusEnum(str, enum.Enum):
    NEW = "New"
    REGISTERED = "Registered"
    CONFIGURED = "Configured"
    ONLINE = "Online"
    MAINTENANCE = "Maintenance"
    OFFLINE = "Offline"
    DECOMMISSIONED = "Decommissioned"'''
    
    content = content.replace(old_enum, new_enum)
    with open('backend/app/models/device.py', 'w') as f:
        f.write(content)

def update_firmware():
    with open('backend/app/models/firmware.py', 'r') as f:
        content = f.read()
        
    if "import enum" not in content:
        content = content.replace("from typing import List, Optional", "import enum\nfrom typing import List, Optional")
    if "Enum" not in content:
        content = content.replace("from sqlalchemy import String, Date, Boolean", "from sqlalchemy import String, Date, Boolean, Enum")
        
    new_enum = '''
class FirmwareStatusEnum(str, enum.Enum):
    DRAFT = "Draft"
    PENDING_APPROVAL = "Pending Approval"
    APPROVED = "Approved"
    DEPLOYED = "Deployed"
    RETIRED = "Retired"

class Firmware(Base):'''
    content = content.replace("class Firmware(Base):", new_enum)
    
    content = content.replace("is_active: Mapped[bool] = mapped_column(Boolean, default=True)", 
                              "is_active: Mapped[bool] = mapped_column(Boolean, default=True)\n    status: Mapped[FirmwareStatusEnum] = mapped_column(Enum(FirmwareStatusEnum), default=FirmwareStatusEnum.DRAFT, nullable=False)")
    
    with open('backend/app/models/firmware.py', 'w') as f:
        f.write(content)

def update_ticket():
    with open('backend/app/models/maintenance_ticket.py', 'r') as f:
        content = f.read()
        
    old_enum = '''class TicketStatusEnum(str, enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"'''
    
    new_enum = '''class TicketStatusEnum(str, enum.Enum):
    OPEN = "Open"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    UNDER_REVIEW = "Under Review"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    REJECTED = "Rejected"'''
    
    content = content.replace(old_enum, new_enum)
    with open('backend/app/models/maintenance_ticket.py', 'w') as f:
        f.write(content)

def update_inventory():
    with open('backend/app/models/inventory.py', 'r') as f:
        content = f.read()
        
    if "import enum" not in content:
        content = content.replace("from typing import Optional", "import enum\nfrom typing import Optional")
    if "Enum" not in content:
        content = content.replace("from sqlalchemy import String, Integer", "from sqlalchemy import String, Integer, Enum")
        
    new_enum = '''
class InventoryStatusEnum(str, enum.Enum):
    CREATED = "Created"
    AVAILABLE = "Available"
    ALLOCATED = "Allocated"
    CONSUMED = "Consumed"
    RESTOCKED = "Restocked"

class Inventory(Base):'''
    content = content.replace("class Inventory(Base):", new_enum)
    
    content = content.replace("supplier: Mapped[Optional[str]] = mapped_column(String(255))",
                              "supplier: Mapped[Optional[str]] = mapped_column(String(255))\n    status: Mapped[InventoryStatusEnum] = mapped_column(Enum(InventoryStatusEnum), default=InventoryStatusEnum.CREATED, nullable=False)")
    
    with open('backend/app/models/inventory.py', 'w') as f:
        f.write(content)

def update_report():
    with open('backend/app/models/report.py', 'r') as f:
        content = f.read()
        
    if "import enum" not in content:
        content = content.replace("from typing import Optional", "import enum\nfrom typing import Optional")
    if "Enum" not in content:
        content = content.replace("from sqlalchemy import String, ForeignKey", "from sqlalchemy import String, ForeignKey, Enum")
        
    new_enum = '''
class ReportStatusEnum(str, enum.Enum):
    DRAFT = "Draft"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    PUBLISHED = "Published"
    ARCHIVED = "Archived"

class Report(Base):'''
    content = content.replace("class Report(Base):", new_enum)
    
    content = content.replace("summary: Mapped[Optional[str]] = mapped_column(String(1000))",
                              "summary: Mapped[Optional[str]] = mapped_column(String(1000))\n    status: Mapped[ReportStatusEnum] = mapped_column(Enum(ReportStatusEnum), default=ReportStatusEnum.DRAFT, nullable=False)")
    
    with open('backend/app/models/report.py', 'w') as f:
        f.write(content)

update_device()
update_firmware()
update_ticket()
update_inventory()
update_report()
print("Success")
