from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Championship(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор чемпионата")
    name: str = Field(..., description="Название чемпионата")
    created_at: datetime = Field(..., description="Дата и время создания чемпионата")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления чемпионата")


class ChampionshipCreate(BaseModel):
    name: str = Field(..., description="Название чемпионата")


class ChampionshipUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название чемпионата")


class ChampionshipDump(BaseModel):
    data: list[Championship] = Field(..., description="Список чемпионатов")
    total_count: int = Field(..., description="Общее количество чемпионатов")
