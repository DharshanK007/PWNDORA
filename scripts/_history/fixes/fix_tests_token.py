import os

filepath = "backend/tests/api/v1/test_milestone_4.py"
with open(filepath, "r") as f: content = f.read()

content = content.replace("superuser_token_headers", "normal_user_token_headers")

with open(filepath, "w") as f: f.write(content)

print("Updated tests token")
