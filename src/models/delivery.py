from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class DeliveryStatus(Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Delivery(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор доставки")
    direction_id: int = Field(..., description="Идентификатор направления")
    name: str = Field(..., description="Название доставки")
    count: int = Field(..., description="Количество товаров для доставки", gt=0)
    status: DeliveryStatus = Field(DeliveryStatus.PENDING, description="Статус доставки")
    created_at: datetime = Field(..., description="Дата и время создания доставки")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления доставки")


class DeliveryCreate(BaseModel):
    direction_id: int = Field(..., description="Идентификатор направления")
    name: str = Field(..., description="Название доставки")
    count: int = Field(..., description="Количество товаров для доставки", gt=0)


class DeliveryUpdate(BaseModel):
    status: DeliveryStatus = Field(DeliveryStatus.PENDING, description="Статус доставки")


class DeliveryDump(BaseModel):
    data: list[Delivery] = Field(..., description="Список доставок")
    total_count: int = Field(..., description="Общее количество доставок")
