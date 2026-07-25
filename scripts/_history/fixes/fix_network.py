import os

filepath = "backend/app/models/network.py"
with open(filepath, "r") as f: content = f.read()
if "trust_level" not in content:
    fields = '''
    trust_level: Mapped[str] = mapped_column(String(50), nullable=True)
    routing_direction: Mapped[str] = mapped_column(String(50), nullable=True)
'''
    content = content.replace('    description: Mapped[str] = mapped_column(String(1000), nullable=True)', '    description: Mapped[str] = mapped_column(String(1000), nullable=True)' + fields)
    with open(filepath, "w") as f: f.write(content)

filepath = "backend/app/schemas/network.py"
with open(filepath, "r") as f: content = f.read()
if "trust_level" not in content:
    fields = '''
    trust_level: Optional[str] = None
    routing_direction: Optional[str] = None
'''
    content = content.replace('    description: Optional[str] = None', '    description: Optional[str] = None' + fields)
    with open(filepath, "w") as f: f.write(content)

print("Updated network schemas")
