import os

filepath = "backend/app/schemas/employee.py"
with open(filepath, "r") as f:
    content = f.read()

example = '''    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "department_id": "123e4567-e89b-12d3-a456-426614174001",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+1234567890",
                "status": "Pending"
            }
        }
    )
'''

if "example" not in content:
    content = content.replace("class EmployeeCreate(EmployeeBase):\n    pass", "class EmployeeCreate(EmployeeBase):\n" + example)

with open(filepath, "w") as f:
    f.write(content)
