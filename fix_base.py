with open('backend/app/services/base.py', 'r') as f:
    content = f.read()

replacement = '''
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        from uuid import UUID
        obj_in_data = obj_in.model_dump()
        obj_in_data = {k: (str(v) if isinstance(v, UUID) else v) for k, v in obj_in_data.items()}
        db_obj = self.model(**obj_in_data)
'''

content = content.replace('''
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
''', replacement)

replacement2 = '''
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        from uuid import UUID
        update_data = {k: (str(v) if isinstance(v, UUID) else v) for k, v in update_data.items()}
'''

content = content.replace('''
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
''', replacement2)

with open('backend/app/services/base.py', 'w') as f:
    f.write(content)
