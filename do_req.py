filepath = "backend/requirements.txt"
with open(filepath, "r") as f: content = f.read()
if "PyYAML" not in content:
    with open(filepath, "a") as f: f.write("\nPyYAML>=6.0.0\n")
    print("Added PyYAML")
