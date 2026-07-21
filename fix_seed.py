import os

filepath = "backend/app/seed/engine.py"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace('role="Admin"', 'role="Administrator"')

with open(filepath, "w") as f:
    f.write(content)

print("Updated seed engine")
