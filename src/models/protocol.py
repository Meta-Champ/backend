from pydantic import BaseModel, Field
from typing import Optional

from enum import Enum


class ProtocolStatus(Enum):
    PUBLISHED = "published"
    ASSIGNED = "assigned"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"


class Protocol(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор протокола")
    direction_id: int = Field(..., description="Идентификатор направления", ge=1)
    name: str = Field(..., description="Название протокола", max_length=32)
    text: str = Field(..., description="Текст протокола")
    status: ProtocolStatus = Field(ProtocolStatus.PUBLISHED, description="Статус протокола")
    assigned_by: list[int] = Field(..., description="Список идентификаторов пользователей, назначивших протокол")
    created_at: int = Field(..., description="Дата и время создания протокола")
    updated_at: int = Field(..., description="Дата и время последнего обновления протокола")


class ProtocolCreate(BaseModel):
    direction_id: int = Field(..., description="Идентификатор направления", ge=1)
    name: str = Field(..., description="Название протокола", max_length=32)
    text: str = Field(..., description="Текст протокола")
    status: ProtocolStatus = Field(ProtocolStatus.PUBLISHED, description="Статус протокола")
    assigned_by: list[int] = Field(..., description="Список идентификаторов пользователей, назначивших протокол")


class ProtocolUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название протокола", max_length=32)
    text: Optional[str] = Field(None, description="Текст протокола")
    status: Optional[ProtocolStatus] = Field(ProtocolStatus.PUBLISHED, description="Статус протокола")
