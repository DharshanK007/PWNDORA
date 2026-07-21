import os

models_dir = "backend/app/models"
files = [f for f in os.listdir(models_dir) if f.endswith(".py") and f != "__init__.py"]

for filename in files:
    filepath = os.path.join(models_dir, filename)
    with open(filepath, "r") as f:
        content = f.read()

    # We want to replace relationship(...) with relationship(..., lazy="selectin")
    # But only if lazy= is not already there.
    # Be careful not to replace something that breaks.
    
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'relationship(' in line and 'lazy=' not in line:
            # find the last ')' and insert ', lazy="selectin"'
            idx = line.rfind(')')
            if idx != -1:
                line = line[:idx] + ', lazy="selectin"' + line[idx:]
        new_lines.append(line)
        
    with open(filepath, "w") as f:
        f.write('\n'.join(new_lines))

print("Updated relationships for eager loading")
