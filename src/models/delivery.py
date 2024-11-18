from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from time import time


class DeliveryStatus(Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Delivery(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор доставки")
    direction_id: int = Field(..., description="Идентификатор направления")
    name: str = Field(..., description="Название доставки")
    count: int = Field(..., description="Количество товаров для доставки")
    status: DeliveryStatus = Field(..., description="Статус доставки")
    created_at: int = Field(..., description="Дата и время создания доставки")
    updated_at: int = Field(..., description="Дата и время последнего обновления доставки")


class DeliveryCreate(BaseModel):
    direction_id: int = Field(..., description="Идентификатор направления")
    name: str = Field(..., description="Название доставки")
    count: int = Field(..., description="Количество товаров для доставки")


class DeliveryUpdate(BaseModel):
    status: DeliveryStatus = Field(..., description="Статус доставки")
