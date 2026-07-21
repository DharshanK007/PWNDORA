import os
import re

filepath = "backend/tests/api/v1/test_workflows.py"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace('"password": "pass"', '"password": "password123"')

with open(filepath, "w") as f:
    f.write(content)
print("Fixed test workflows passwords")
