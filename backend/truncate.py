from app.db.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()
db.execute(text('TRUNCATE TABLE notifications CASCADE;'))
db.commit()
print("Truncated")
