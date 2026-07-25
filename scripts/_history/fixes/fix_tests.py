import os

filepath = "backend/tests/api/v1/test_milestone_4.py"
with open(filepath, "r") as f: content = f.read()

content = content.replace(
    'res = client.get(f"{settings.API_V1_STR}/scenarios/")',
    'res = client.get(f"{settings.API_V1_STR}/scenarios/scenario_001/registry")'
)
content = content.replace(
    'assert isinstance(data, list)',
    'assert isinstance(data, dict)'
)
content = content.replace(
    'assert len(data) > 0\\n    assert data[0]["id"] == "scenario_001"',
    'assert data["id"] == "scenario_001"'
)

with open(filepath, "w") as f: f.write(content)

print("Updated tests")
