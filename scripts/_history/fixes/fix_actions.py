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

    # Import ActionResponse
    if "from app.schemas.response import" not in content:
        content = "from app.schemas.response import ActionResponse\n" + content
    
    # We want to find endpoints like @router.post("/{id}/workflow"
    # and update their response model.
    
    lines = content.split('\n')
    new_lines = []
    in_workflow_action = False
    for line in lines:
        if 'router.post("/login/access-token"' in line and filename == "auth.py":
            # Just for login, actually login returns a specific Token model.
            pass
            
        if 'router.post("/{id}/workflow"' in line or 'router.post("/{id}/activate"' in line or 'router.post("/{id}/approve"' in line:
            # We found a custom action
            # We need to change the response_model
            # E.g., @router.post("/{id}/workflow", response_model=EmployeeResponse)
            # Find the response_model=... and replace it
            match = re.search(r'response_model=([a-zA-Z]+)', line)
            if match:
                model_name = match.group(1)
                line = line.replace(f"response_model={model_name}", f"response_model=ActionResponse[{model_name}]")
            in_workflow_action = True
            new_lines.append(line)
            continue
            
        if in_workflow_action and 'return ' in line and 'def ' not in line:
            # Wrap the return value in ActionResponse
            # Assuming it looks like eturn employee_obj
            # Wait, there might be multiple returns or we might miss something.
            # Usually it's eturn updated_obj
            # Let's use a regex to capture the return value
            match = re.search(r'return (.*)', line)
            if match:
                ret_val = match.group(1).strip()
                line = line.replace(f"return {ret_val}", f"return ActionResponse(success=True, message='Action successful', data={ret_val})")
            in_workflow_action = False
            
        new_lines.append(line)
        
    with open(filepath, "w") as f:
        f.write('\n'.join(new_lines))

print("Updated ActionResponse wrappers")
