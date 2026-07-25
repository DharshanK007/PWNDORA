import os

filepath = "backend/app/main.py"
with open(filepath, "r") as f: content = f.read()

if "manager.load_all" not in content:
    content += '''
@app.on_event("startup")
def startup_event():
    import os
    from app.scenarios.scenario_manager import manager
    data_dir = os.path.join(os.path.dirname(__file__), "scenario_data")
    manager.load_all(data_dir)
    print(f"Loaded {len(manager.registry.list_scenarios())} scenarios")
'''
    with open(filepath, "w") as f: f.write(content)

print("Updated main.py")
