import os

data_dir = "backend/app/scenario_data/scenario_001"
os.makedirs(os.path.join(data_dir, "metadata"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "resources"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "documents"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "logs"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "configs"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "backups"), exist_ok=True)

yaml_content = '''id: "scenario_001"
name: "Production Line Firmware Failure"
category: "Configuration"
difficulty: "Beginner"
required_role: "Engineer"
business_context: "Production Line 2 has stopped responding after a failed firmware deployment. Investigate the root cause."
stages:
  - id: 1
    objective: "Read the maintenance ticket."
    required_action: "Fetch clue ticket_001"
    next_stage: 2
  - id: 2
    objective: "Analyze deployment log."
    required_action: "Fetch clue log_001"
    next_stage: 3
  - id: 3
    objective: "Find leaked config backup."
    required_action: "Fetch clue config_backup"
    next_stage: 4
  - id: 4
    objective: "Exploit vulnerable admin endpoint."
    required_action: "POST /auth/login with admin"
    next_stage: null
'''
with open(os.path.join(data_dir, "scenario.yaml"), "w") as f: f.write(yaml_content)

print("Created scenario data")
