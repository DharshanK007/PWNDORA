import os

filepath = "backend/app/services/base.py"
with open(filepath, "r") as f:
    content = f.read()

# Make sure query params are imported
if "from app.api.dependencies.query" not in content:
    content = "from app.api.dependencies.query import QueryParameters, CursorQueryParameters\n" + content

# Replace get_multi
old_get_multi = '''    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_count(self, db: Session) -> int:
        return db.query(self.model).count()'''

new_get_multi = '''    def _apply_query_params(self, query, params: QueryParameters):
        if params.status and hasattr(self.model, "status"):
            query = query.filter(self.model.status == params.status)
        if params.search:
            # Try to search by a 'name' or 'title' or 'email' column if it exists
            search_col = getattr(self.model, "name", None) or getattr(self.model, "title", None) or getattr(self.model, "email", None)
            if search_col is not None:
                query = query.filter(search_col.ilike(f"%{params.search}%"))
        
        # Sort
        sort_col = getattr(self.model, params.sort_by, None) if params.sort_by else getattr(self.model, "created_at", None)
        if sort_col is not None:
            if params.sort_order == "desc":
                query = query.order_by(sort_col.desc())
            else:
                query = query.order_by(sort_col.asc())
        return query

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, params: Optional[QueryParameters] = None) -> List[ModelType]:
        query = db.query(self.model)
        if params:
            query = self._apply_query_params(query, params)
            skip = params.skip
            limit = params.limit
        return query.offset(skip).limit(limit).all()

    def get_count(self, db: Session, params: Optional[QueryParameters] = None) -> int:
        query = db.query(self.model)
        if params:
            query = self._apply_query_params(query, params)
        return query.count()

    def get_multi_cursor(self, db: Session, *, params: CursorQueryParameters) -> List[ModelType]:
        query = db.query(self.model)
        
        if params.search:
            search_col = getattr(self.model, "name", None) or getattr(self.model, "title", None) or getattr(self.model, "email", None)
            if search_col is not None:
                query = query.filter(search_col.ilike(f"%{params.search}%"))
                
        sort_col = getattr(self.model, "id", getattr(self.model, "created_at", None))
        
        if params.cursor and sort_col is not None:
            if params.sort_order == "desc":
                query = query.filter(sort_col < params.cursor)
            else:
                query = query.filter(sort_col > params.cursor)
                
        if sort_col is not None:
            if params.sort_order == "desc":
                query = query.order_by(sort_col.desc())
            else:
                query = query.order_by(sort_col.asc())
                
        return query.limit(params.limit).all()'''

content = content.replace(old_get_multi, new_get_multi)

with open(filepath, "w") as f:
    f.write(content)
print("Updated base.py")
