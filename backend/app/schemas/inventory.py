from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.inventory import InventoryStatusEnum
from datetime import datetime
from uuid import UUID

class InventoryBase(BaseModel):
    component_name: str
    part_number: str
    stock_quantity: int = Field(0, ge=0)
    warehouse_zone: Optional[str] = None
    supplier: Optional[str] = None
    status: Optional[InventoryStatusEnum] = None
    status: InventoryStatusEnum = InventoryStatusEnum.CREATED

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    component_name: Optional[str] = None
    part_number: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    warehouse_zone: Optional[str] = None
    supplier: Optional[str] = None
    status: Optional[InventoryStatusEnum] = None
    status: InventoryStatusEnum = InventoryStatusEnum.CREATED

class InventoryResponse(InventoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
