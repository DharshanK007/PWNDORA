import os

# 1. Update Model
model_path = "backend/app/models/employee.py"
with open(model_path, "r") as f:
    model_content = f.read()

fields_to_add = '''
    title: Mapped[Optional[str]] = mapped_column(String(100))
    shift: Mapped[Optional[str]] = mapped_column(String(50))
    office: Mapped[Optional[str]] = mapped_column(String(100))
    skills: Mapped[Optional[list]] = mapped_column(JSON)
    manager_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("employees.id"))

    manager: Mapped[Optional["Employee"]] = relationship("Employee", remote_side="Employee.id", backref="direct_reports")
'''

if "manager_id" not in model_content:
    if "from sqlalchemy import String, ForeignKey, Enum" in model_content:
        model_content = model_content.replace("from sqlalchemy import String, ForeignKey, Enum", "from sqlalchemy import String, ForeignKey, Enum, JSON")
    
    # insert before user: Mapped
    model_content = model_content.replace('    user: Mapped["User"]', fields_to_add + '    user: Mapped["User"]')
    
    with open(model_path, "w") as f:
        f.write(model_content)

# 2. Update Schema
schema_path = "backend/app/schemas/employee.py"
with open(schema_path, "r") as f:
    schema_content = f.read()

schema_fields_base = '''
    title: Optional[str] = None
    shift: Optional[str] = None
    office: Optional[str] = None
    skills: Optional[list] = None
    manager_id: Optional[UUID] = None
'''

if "manager_id" not in schema_content:
    schema_content = schema_content.replace('    phone: Optional[str]', schema_fields_base + '    phone: Optional[str]')
    schema_content = schema_content.replace('    phone: Optional[str] = Field(None, pattern=r"^\\+?[1-9]\\d{1,14}$")', schema_fields_base + '    phone: Optional[str] = Field(None, pattern=r"^\\+?[1-9]\\d{1,14}$")')
    
    # Update UpdateSchema too
    schema_content = schema_content.replace('    first_name: Optional[str] = Field', schema_fields_base + '    first_name: Optional[str] = Field')
    
    with open(schema_path, "w") as f:
        f.write(schema_content)

print("Phase 2 & 3 schemas updated")
