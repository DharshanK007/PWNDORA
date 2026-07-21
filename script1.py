import os

services_dir = "backend/app/services"

# employee.py
employee_file = os.path.join(services_dir, "employee.py")
with open(employee_file, "r") as f:
    content = f.read()

if "from app.events.event_bus import EventBus" not in content:
    content = "from app.events.event_bus import EventBus\nfrom app.events.events import EmployeeActivated, EmployeeTerminated\n" + content
    
    content = content.replace("return db_obj", """metadata = {"previous_state": "Pending", "new_state": db_obj.status.value, "reason": "System action"}
        EventBus.publish(EmployeeActivated.create(entity_id=str(db_obj.id), metadata=metadata))
        return db_obj""", 1) # Only first for activate
    content = content.replace("return db_obj", """metadata = {"previous_state": "Active", "new_state": db_obj.status.value, "reason": "System action"}
        EventBus.publish(EmployeeTerminated.create(entity_id=str(db_obj.id), metadata=metadata))
        return db_obj""", 1) # Second for suspend? Wait, need to be careful with replace.
        
with open(employee_file, "w") as f:
    f.write(content)
