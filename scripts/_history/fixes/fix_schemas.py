import os

schema_dir = "backend/app/schemas"
files = [
    ("employee.py", [
        ("first_name: str", 'first_name: str = Field(..., min_length=2, max_length=50)'),
        ("last_name: str", 'last_name: str = Field(..., min_length=2, max_length=50)'),
        ("first_name: Optional[str] = None", 'first_name: Optional[str] = Field(None, min_length=2, max_length=50)'),
        ("last_name: Optional[str] = None", 'last_name: Optional[str] = Field(None, min_length=2, max_length=50)'),
        ("phone: Optional[str] = None", 'phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")')
    ]),
    ("department.py", [
        ("name: str", 'name: str = Field(..., min_length=2, max_length=100)'),
        ("name: Optional[str] = None", 'name: Optional[str] = Field(None, min_length=2, max_length=100)')
    ]),
    ("device.py", [
        ("name: str", 'name: str = Field(..., min_length=2, max_length=100)'),
        ("name: Optional[str] = None", 'name: Optional[str] = Field(None, min_length=2, max_length=100)'),
        ("ip_address: Optional[str] = None", 'ip_address: Optional[str] = Field(None, pattern=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")')
    ]),
    ("firmware.py", [
        ("version: str", 'version: str = Field(..., min_length=1, max_length=50)'),
        ("version: Optional[str] = None", 'version: Optional[str] = Field(None, min_length=1, max_length=50)'),
        ("release_notes: Optional[str] = None", 'release_notes: Optional[str] = Field(None, max_length=1000)')
    ]),
    ("machine_location.py", [
        ("name: str", 'name: str = Field(..., min_length=2, max_length=100)'),
        ("name: Optional[str] = None", 'name: Optional[str] = Field(None, min_length=2, max_length=100)'),
        ("building: str", 'building: str = Field(..., min_length=2, max_length=100)'),
        ("building: Optional[str] = None", 'building: Optional[str] = Field(None, min_length=2, max_length=100)')
    ]),
    ("maintenance_ticket.py", [
        ("title: str", 'title: str = Field(..., min_length=5, max_length=100)'),
        ("title: Optional[str] = None", 'title: Optional[str] = Field(None, min_length=5, max_length=100)'),
        ("description: str", 'description: str = Field(..., min_length=10, max_length=2000)'),
        ("description: Optional[str] = None", 'description: Optional[str] = Field(None, min_length=10, max_length=2000)')
    ]),
    ("inventory.py", [
        ("part_name: str", 'part_name: str = Field(..., min_length=2, max_length=100)'),
        ("part_name: Optional[str] = None", 'part_name: Optional[str] = Field(None, min_length=2, max_length=100)'),
        ("quantity: int", 'quantity: int = Field(..., ge=0)'),
        ("quantity: Optional[int] = None", 'quantity: Optional[int] = Field(None, ge=0)'),
        ("minimum_stock_level: int", 'minimum_stock_level: int = Field(..., ge=0)'),
        ("minimum_stock_level: Optional[int] = None", 'minimum_stock_level: Optional[int] = Field(None, ge=0)')
    ]),
    ("report.py", [
        ("title: str", 'title: str = Field(..., min_length=3, max_length=200)'),
        ("title: Optional[str] = None", 'title: Optional[str] = Field(None, min_length=3, max_length=200)')
    ])
]

for filename, replacements in files:
    filepath = os.path.join(schema_dir, filename)
    with open(filepath, "r") as f:
        code = f.read()
    
    if "from pydantic import" in code and "Field" not in code:
        code = code.replace("from pydantic import BaseModel", "from pydantic import BaseModel, Field")
    elif "from pydantic import BaseModel, ConfigDict" in code and "Field" not in code:
        code = code.replace("from pydantic import BaseModel, ConfigDict", "from pydantic import BaseModel, ConfigDict, Field")
    
    for old, new in replacements:
        code = code.replace(old, new)
        
    with open(filepath, "w") as f:
        f.write(code)
    print(f"Updated {filename}")
