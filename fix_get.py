with open('backend/app/services/base.py', 'r') as f:
    content = f.read()

replacement = '''
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        from uuid import UUID
        if isinstance(id, UUID): id = str(id)
        return db.query(self.model).filter(self.model.id == id).first()
'''
content = content.replace('''
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()
''', replacement)

replacement2 = '''
    def remove(self, db: Session, *, id: Any) -> ModelType:
        from uuid import UUID
        if isinstance(id, UUID): id = str(id)
        obj = db.query(self.model).get(id)
        db.delete(obj)
'''
content = content.replace('''
    def remove(self, db: Session, *, id: Any) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
''', replacement2)

with open('backend/app/services/base.py', 'w') as f:
    f.write(content)
