import os

filepath = "backend/app/scenarios/scenario_model.py"
with open(filepath, "r") as f: content = f.read()

if "states: Mapped[list[\\"ScenarioState\\"]]" not in content:
    content = content.replace(
        "affected_assets: Mapped[list] = mapped_column(JSON, nullable=True)", 
        "affected_assets: Mapped[list] = mapped_column(JSON, nullable=True)\n    states: Mapped[list[\\"ScenarioState\\"]] = relationship(\\"ScenarioState\\", back_populates=\\"scenario\\", cascade=\\"all, delete-orphan\\")"
    )
    with open(filepath, "w") as f: f.write(content)

filepath = "backend/app/models/user.py"
with open(filepath, "r") as f: content = f.read()

if "scenario_states: Mapped[list[\\"ScenarioState\\"]]" not in content:
    content = content.replace(
        "role_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey(\\"roles.id\\"))", 
        "role_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey(\\"roles.id\\"))\n    scenario_states: Mapped[list[\\"ScenarioState\\"]] = relationship(\\"ScenarioState\\", back_populates=\\"user\\", cascade=\\"all, delete-orphan\\")"
    )
    with open(filepath, "w") as f: f.write(content)

filepath = "backend/app/db/base.py"
with open(filepath, "r") as f: content = f.read()
if "ScenarioState" not in content:
    content += "\nfrom app.scenarios.scenario_state_model import ScenarioState"
    with open(filepath, "w") as f: f.write(content)

print("Updated relations and base")
