import os

filepath = "backend/app/seed/maintenance_seed.py"
with open(filepath, "r") as f: content = f.read()

content = content.replace("title=f\\"Maintenance for {fake.word()}\\",\\n            description=fake.text(),", "issue_description=f\\"Maintenance for {fake.word()}: {fake.text()[:50]}\\",")
with open(filepath, "w") as f: f.write(content)

print("Fixed maintenance seed")
