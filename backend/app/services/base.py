from app.api.dependencies.query import QueryParameters, CursorQueryParameters
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        from uuid import UUID
        if isinstance(id, UUID): id = str(id)
        return db.query(self.model).filter(self.model.id == id).first()

    def _apply_query_params(self, query, params: QueryParameters):
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
                
        return query.limit(params.limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        from uuid import UUID
        obj_in_data = obj_in.model_dump()
        obj_in_data = {k: (str(v) if isinstance(v, UUID) else v) for k, v in obj_in_data.items()}
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = {
            c.name: getattr(db_obj, c.name) 
            for c in db_obj.__table__.columns
        }
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        from uuid import UUID
        update_data = {k: (str(v) if isinstance(v, UUID) else v) for k, v in update_data.items()}
            
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: Any) -> ModelType:
        from uuid import UUID
        if isinstance(id, UUID): id = str(id)
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
