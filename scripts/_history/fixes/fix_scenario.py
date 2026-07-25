import os

# Update Scenario Model
filepath = "backend/app/scenarios/scenario_model.py"
with open(filepath, "r") as f: content = f.read()
if "business_impact" not in content:
    content = content.replace('    scenario_type: Mapped[str] = mapped_column(String(100), nullable=True)', '    scenario_type: Mapped[str] = mapped_column(String(100), nullable=True)\n    business_impact: Mapped[str] = mapped_column(String(100), nullable=True)')
    with open(filepath, "w") as f: f.write(content)

# Update Scenario Schema
filepath = "backend/app/scenarios/scenario_schema.py"
with open(filepath, "r") as f: content = f.read()
if "business_impact" not in content:
    content = content.replace('    scenario_type: Optional[str] = None', '    scenario_type: Optional[str] = None\n    business_impact: Optional[str] = None')
    with open(filepath, "w") as f: f.write(content)

print("Added business impact")
