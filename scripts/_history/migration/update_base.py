base_py = "backend/app/db/base.py"
with open(base_py, "a") as f:
    f.write('''
from app.audit.audit_models import AuditLog
from app.models.notification import Notification
from app.models.workflow_history import WorkflowHistory
''')

print("Added models to base.py")
