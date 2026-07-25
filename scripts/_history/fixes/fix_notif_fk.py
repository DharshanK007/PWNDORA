import os

file_path = "backend/app/models/notification.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace(
    "from sqlalchemy import String, Boolean, DateTime, Text, Enum",
    "from sqlalchemy import String, Boolean, DateTime, Text, Enum, ForeignKey"
)
content = content.replace(
    "recipient_id: Mapped[str] = mapped_column(String(36), index=True, nullable=True) # None = Broadcast",
    "recipient_id: Mapped[str] = mapped_column(String(36), ForeignKey('users.id'), index=True, nullable=True) # None = Broadcast"
)

with open(file_path, "w") as f:
    f.write(content)

print("Added foreign key to notification.")
