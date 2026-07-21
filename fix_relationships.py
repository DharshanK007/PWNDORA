import os

notif_file = "backend/app/models/notification.py"
with open(notif_file, "r") as f:
    content = f.read()

if "relationship" not in content:
    content = content.replace(
        "from sqlalchemy.orm import Mapped, mapped_column",
        "from sqlalchemy.orm import Mapped, mapped_column, relationship\nfrom typing import Optional"
    )
    # The models might not be fully loaded, avoid circular import with string "User"
    content += "\n    recipient: Mapped[Optional['User']] = relationship(back_populates='notifications')\n"
    with open(notif_file, "w") as f:
        f.write(content)

user_file = "backend/app/models/user.py"
with open(user_file, "r") as f:
    content = f.read()

content = content.replace(
    "notifications: Mapped[List[\"Notification\"]] = relationship(back_populates=\"user\")",
    "notifications: Mapped[List[\"Notification\"]] = relationship(back_populates=\"recipient\", foreign_keys='Notification.recipient_id')"
)

with open(user_file, "w") as f:
    f.write(content)
