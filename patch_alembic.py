import os
import re

file_path = "backend/alembic/versions/c24829d7ca3d_milestone_3b_tables.py"
with open(file_path, "r") as f:
    content = f.read()

# Add the enum creation logic
enum_create = "    sa.Enum('INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL', name='notificationseverityenum').create(op.get_bind())\n    op.add_column"
content = content.replace("op.add_column", enum_create, 1)

with open(file_path, "w") as f:
    f.write(content)

print("Patched alembic migration.")
