import os

# fix service
service_file = "backend/app/services/notification.py"
with open(service_file, "r") as f:
    content = f.read()

content = content.replace("NotificationService = CRUDNotification(Notification)", "notification = CRUDNotification(Notification)")
with open(service_file, "w") as f:
    f.write(content)

# fix api
api_file = "backend/app/api/v1/endpoints/notifications.py"
with open(api_file, "r") as f:
    content = f.read()

content = content.replace("from app.services.notification import NotificationService", "from app.services.notification import notification")
content = content.replace("NotificationService.model", "notification.model")
content = content.replace("NotificationService.get", "notification.get")
content = content.replace("NotificationService.mark_read", "notification.mark_read")
with open(api_file, "w") as f:
    f.write(content)
