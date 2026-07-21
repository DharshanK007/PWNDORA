import os
import re

endpoints_dir = "backend/app/api/v1/endpoints"
files_to_update = ["employees.py", "inventory.py", "firmwares.py", "devices.py", "tickets.py", "auth.py"]

for filename in files_to_update:
    filepath = os.path.join(endpoints_dir, filename)
    if not os.path.exists(filepath):
        continue
    with open(filepath, "r") as f:
        content = f.read()

    if "ActionResponse" not in content:
        content = "from app.schemas.response import ActionResponse\n" + content

    lines = content.split('\n')
    new_lines = []
    
    in_action = False
    
    for i, line in enumerate(lines):
        if filename != "auth.py" and '@router.post("/{id}/' in line:
            # Found a workflow action
            in_action = True
            line = re.sub(r'response_model=([a-zA-Z]+)', r'response_model=ActionResponse[\1]', line)
        
        elif filename == "auth.py" and '@router.post("/login/access-token"' in line:
            in_action = True
            line = re.sub(r'response_model=([a-zA-Z]+)', r'response_model=ActionResponse[\1]', line)
            
        elif in_action and line.strip().startswith('return ') and 'def ' not in line:
            # Replace return <obj> with ActionResponse
            obj = line.strip().split('return ')[1]
            line = line.replace(f"return {obj}", f"return ActionResponse(success=True, message='Action successful', data={obj})")
            in_action = False
            
        new_lines.append(line)

    with open(filepath, "w") as f:
        f.write('\n'.join(new_lines))
        
print("Successfully wrapped action responses")
