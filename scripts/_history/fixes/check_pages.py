# Fix ScenarioDetailPage - change placeholder text since it imports Construction
import os

for root, dirs, files in os.walk("frontend/src/pages"):
    for fname in files:
        fp = os.path.join(root, fname)
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        # Check if it has Construction import but uses the generated pattern
        if "Construction" in content:
            print(f"OK: {fp}")
        
print("Check done")
