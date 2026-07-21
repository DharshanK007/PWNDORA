import os
import re

schema_dir = "backend/app/schemas"

# Let's write specific replacements for user.py first
user_path = os.path.join(schema_dir, "user.py")
with open(user_path, "r") as f:
    user_code = f.read()

# Make sure Field and EmailStr are imported
if "from pydantic import" in user_code and "Field" not in user_code:
    user_code = user_code.replace("from pydantic import BaseModel", "from pydantic import BaseModel, Field, EmailStr")

user_code = user_code.replace("email: str", "email: EmailStr")
user_code = user_code.replace("password: str", 'password: str = Field(..., min_length=8, max_length=128)')
user_code = user_code.replace("password: Optional[str] = None", 'password: Optional[str] = Field(None, min_length=8, max_length=128)')

with open(user_path, "w") as f:
    f.write(user_code)

print("Updated user.py")
