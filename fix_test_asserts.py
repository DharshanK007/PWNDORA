import os

filepath = "backend/tests/api/v1/test_workflows.py"
with open(filepath, "r") as f:
    content = f.read()

# Replace .json()["status"] -> .json()["data"]["status"] but only for the actions (activate, allocate, etc.)
# Because emp_res.json()["status"] for create returns standard response without wrapper.
# Wait, did I wrap emp_res? No, create returns direct model.
content = content.replace('act_res.json()["status"]', 'act_res.json()["data"]["status"]')
content = content.replace('alloc_res.json()["status"]', 'alloc_res.json()["data"]["status"]')
content = content.replace('act_res.json()["status"]', 'act_res.json()["data"]["status"]') # just in case

with open(filepath, "w") as f:
    f.write(content)
print("Updated test_workflows assertions")
